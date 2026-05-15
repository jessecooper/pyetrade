# E*TRADE OAuth with pyetrade: Quirks & Workarounds

This guide documents known issues and workarounds when integrating pyetrade with E*TRADE OAuth authentication. Many of these quirks are undocumented in official pyetrade docs and cause issues for new users.

## Table of Contents
1. [Parameter Name Confusion](#parameter-name-confusion)
2. [OAuth Flow Issues](#oauth-flow-issues)
3. [Token Endpoint Quirks](#token-endpoint-quirks)
4. [Token Encoding](#token-encoding)
5. [API Response Variance](#api-response-variance)
6. [Complete Working Example](#complete-working-example)

---

## Parameter Name Confusion

**The Problem:** pyetrade parameter names differ from E*TRADE API documentation, causing confusion and errors.

**Mapping Table:**

| pyetrade Parameter | E*TRADE Docs Name | Used In | Notes |
|---|---|---|---|
| `client_key` | `consumer_key` | OAuth init | pyetrade uses different name |
| `client_secret` | `consumer_secret` | OAuth init | pyetrade uses different name |
| `resource_owner_key` | `oauth_token` | API calls | Token obtained during auth |
| `resource_owner_secret` | `oauth_token_secret` | API calls | Token secret obtained during auth |
| `dev=True` | Sandbox | Quote/order endpoints | Use for testing |
| `dev=False` | Production | Quote/order endpoints | Use for real trades |

**Example:**
```python
from pyetrade import ETradeAccounts

# CORRECT (pyetrade naming)
accounts = ETradeAccounts(
    client_key="YOUR_CONSUMER_KEY",
    client_secret="YOUR_CONSUMER_SECRET",
    resource_owner_key="oauth_token_value",
    resource_owner_secret="oauth_token_secret_value",
    dev=False  # Production
)

# WRONG - Will fail
accounts = ETradeAccounts(
    consumer_key="YOUR_CONSUMER_KEY",  # Wrong parameter name
    consumer_secret="YOUR_CONSUMER_SECRET",  # Wrong parameter name
    dev=False
)
```

---

## OAuth Flow Issues

**The Problem:** pyetrade's built-in OAuth flow doesn't work with E*TRADE's requirements. The library assumes a standard OAuth 1.0a flow, but E*TRADE has specific requirements that break the built-in implementation.

### Why Built-in Flow Fails

E*TRADE requires:
- `callback_uri="oob"` (out-of-band) in the OAuth header
- Specific token endpoint URLs
- URL-decoded tokens
- Browser-based PIN approval

pyetrade's built-in `get_request_token()` and related methods don't handle these requirements correctly.

### Solution: Custom OAuth Handler

Implement a custom OAuth handler that:
1. Uses `requests-oauthlib` directly
2. Properly formats the OAuth header with `callback_uri="oob"`
3. Handles E*TRADE's token endpoints
4. Decodes URL-encoded tokens
5. Manages token persistence (e.g., via Windows Keyring)

**Example Custom Handler Structure:**
```python
from requests_oauthlib import OAuth1Session
import urllib.parse

class ETradeOAuthHandler:
    def __init__(self, consumer_key, consumer_secret, env="prod"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.env = env
        self.base_url = "https://api.etrade.com"
    
    def get_request_token(self):
        """Get request token with proper callback_uri handling."""
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            callback_uri="oob"  # CRITICAL: out-of-band
        )
        
        request_token_url = f"{self.base_url}/oauth/request_token"
        tokens = oauth.fetch_request_token(request_token_url)
        
        return {
            "oauth_token": tokens.get("oauth_token"),
            "oauth_token_secret": tokens.get("oauth_token_secret")
        }
    
    def get_access_token(self, oauth_token, oauth_token_secret, pin):
        """Exchange request token + PIN for access token."""
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=oauth_token,
            resource_owner_secret=oauth_token_secret,
            verifier=pin
        )
        
        access_token_url = f"{self.base_url}/oauth/access_token"
        tokens = oauth.fetch_access_token(access_token_url)
        
        return {
            "oauth_token": urllib.parse.unquote(tokens.get("oauth_token")),
            "oauth_token_secret": urllib.parse.unquote(tokens.get("oauth_token_secret"))
        }
```

---

## Token Endpoint Quirks

**The Problem:** E*TRADE's OAuth endpoints don't follow standard conventions, and sandbox/production behave unexpectedly.

### Endpoint Rules

| Operation | Sandbox URL | Production URL | Notes |
|---|---|---|---|
| Request Token | `https://api.etrade.com/oauth/request_token` | `https://api.etrade.com/oauth/request_token` | Always use `api.etrade.com`, never `apisb` |
| Authorize | Browser opens E*TRADE login | Browser opens E*TRADE login | Same for both environments |
| Access Token | `https://api.etrade.com/oauth/access_token` | `https://api.etrade.com/oauth/access_token` | Always use `api.etrade.com`, never `apisb` |
| Data Calls (Quotes, Orders, etc.) | `https://apisb.etrade.com/...` | `https://api.etrade.com/...` | Only here does sandbox differ |

**Key Takeaway:** Token endpoints always use `https://api.etrade.com`, regardless of sandbox/production. Only data calls use `apisb` for sandbox.

---

## Token Encoding

**The Problem:** E*TRADE returns URL-encoded tokens (e.g., spaces become `%20`), but developers often forget to decode them.

### The Issue
```python
# E*TRADE returns: "oauth_token=ABC%20XYZ"
# If you use the raw value: "ABC%20XYZ" (WRONG)
# Decoded value: "ABC XYZ" (CORRECT)
```

Using the wrong token causes authentication failures that are hard to debug.

### Solution: Always Decode
```python
import urllib.parse

# After getting tokens from E*TRADE
oauth_token = urllib.parse.unquote(raw_token)
oauth_token_secret = urllib.parse.unquote(raw_secret)
```

**Apply this to all tokens returned by E*TRADE API calls.**

---

## API Response Variance

**The Problem:** pyetrade sometimes returns API responses as a list instead of a dict, causing `list indices must be integers or slices, not str` errors.

### Example Error
```python
# Expected (dict):
response = {
    "PreviewOrderResponse": {
        "PreviewIds": {"previewId": "12345"}
    }
}

# Sometimes received (list):
response = [
    {
        "PreviewOrderResponse": {
            "PreviewIds": {"previewId": "12345"}
        }
    }
]

# Direct dict access fails:
preview_id = response["PreviewOrderResponse"]  # TypeError!
```

### Solution: Normalize Responses

Create helper functions to unwrap list responses:
```python
def normalize(obj):
    """If pyetrade returns a list instead of a dict, unwrap it."""
    if isinstance(obj, list):
        return obj[0] if obj else {}
    return obj


def safe_get(obj, *keys):
    """
    Traverse nested keys safely, unwrapping any lists along the way.
    
    Example:
        safe_get(response, "PreviewOrderResponse", "PreviewIds", "previewId")
    """
    for key in keys:
        if obj is None:
            return None
        obj = normalize(obj)
        obj = obj.get(key)
    return normalize(obj) if isinstance(obj, (list, dict)) else obj


# Usage in pyetrade calls:
preview = normalize(orders_client.preview_equity_order(**params))
preview_id = safe_get(preview, "PreviewOrderResponse", "PreviewIds", "previewId")

if preview_id is None:
    raise ValueError(f"Could not extract previewId from response: {preview}")
```

**Apply normalization to ALL pyetrade API responses** that you parse.

---

## Complete Working Example

Here's a minimal, working example that demonstrates all the quirks and how to handle them:
```python
import urllib.parse
from requests_oauthlib import OAuth1Session
from pyetrade import ETradeOrder
import webbrowser
import keyring
import json

class ETradeOAuthManager:
    """Handles E*TRADE OAuth with workarounds for known pyetrade quirks."""
    
    def __init__(self, consumer_key, consumer_secret, env="sandbox"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.env = env
        self.base_url = "https://api.etrade.com"
    
    def get_request_token(self):
        """Get request token (quirk: callback_uri must be in header)."""
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            callback_uri="oob"  # Critical for E*TRADE
        )
        
        request_token_url = f"{self.base_url}/oauth/request_token"
        tokens = oauth.fetch_request_token(request_token_url)
        
        return tokens.get("oauth_token"), tokens.get("oauth_token_secret")
    
    def get_access_token(self, request_token, request_token_secret, pin):
        """Exchange request token + PIN for access token (quirk: URL decode tokens)."""
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=request_token,
            resource_owner_secret=request_token_secret,
            verifier=pin
        )
        
        access_token_url = f"{self.base_url}/oauth/access_token"
        tokens = oauth.fetch_access_token(access_token_url)
        
        # CRITICAL: E*TRADE returns URL-encoded tokens
        return (
            urllib.parse.unquote(tokens.get("oauth_token")),
            urllib.parse.unquote(tokens.get("oauth_token_secret"))
        )
    
    def authenticate(self):
        """Full OAuth flow: request token → PIN → access token."""
        print("Step 1: Get request token...")
        req_token, req_secret = self.get_request_token()
        
        print("Step 2: Open browser for authorization...")
        auth_url = f"https://us.etrade.com/e/t/user/oauth/authorize?key={req_token}"
        webbrowser.open(auth_url)
        
        pin = input("Enter the PIN from E*TRADE: ").strip()
        
        print("Step 3: Exchange for access token...")
        access_token, access_secret = self.get_access_token(req_token, req_secret, pin)
        
        # Cache tokens (example using keyring)
        keyring.set_password("etrade", "oauth_token", access_token)
        keyring.set_password("etrade", "oauth_token_secret", access_secret)
        
        return access_token, access_secret


def normalize(obj):
    """Handle pyetrade list/dict variance."""
    if isinstance(obj, list):
        return obj[0] if obj else {}
    return obj


def safe_get(obj, *keys):
    """Safely traverse nested keys with list unwrapping."""
    for key in keys:
        if obj is None:
            return None
        obj = normalize(obj)
        obj = obj.get(key)
    return normalize(obj) if isinstance(obj, (list, dict)) else obj


# Usage
if __name__ == "__main__":
    oauth_mgr = ETradeOAuthManager(
        consumer_key="YOUR_KEY",
        consumer_secret="YOUR_SECRET",
        env="prod"
    )
    
    # First time: authenticate and cache tokens
    access_token, access_secret = oauth_mgr.authenticate()
    
    # Create order client (quirk: use pyetrade parameter names)
    orders = ETradeOrder(
        client_key="YOUR_KEY",  # NOT consumer_key
        client_secret="YOUR_SECRET",  # NOT consumer_secret
        resource_owner_key=access_token,  # NOT oauth_token
        resource_owner_secret=access_secret,  # NOT oauth_token_secret
        dev=False  # Production
    )
    
    # Preview an order (quirk: normalize response)
    preview_resp = normalize(orders.preview_equity_order(
        accountIdKey="12345",
        clientOrderId="order_1",
        PreviewIds="0",
        order=[{
            "symbolType": "EQ",
            "orderType": "EQ",
            "clientOrderId": "order_1",
            "Order": {
                "allOrNone": False,
                "goodForDay": True,
                "marketSession": "REGULAR",
                "orderType": "EQ",
                "clientOrderId": "order_1",
                "Order": [
                    {
                        "symbol": "AAPL",
                        "quantity": 10,
                        "orderType": "BUY",
                        "limitPrice": 150.00,
                        "stopPrice": 0.00,
                        "allOrNone": False,
                        "goodForDay": True
                    }
                ]
            }
        }]
    ))
    
    # Extract with safe_get (quirk: handle nested variance)
    preview_id = safe_get(preview_resp, "PreviewOrderResponse", "PreviewIds", "previewId")
    commission = safe_get(preview_resp, "PreviewOrderResponse", "Order", "estimatedCommission")
    
    print(f"Preview ID: {preview_id}, Commission: ${commission}")
```

---

## Summary

When using pyetrade with E*TRADE:

✅ **Do:**
- Use `client_key`, `client_secret`, `resource_owner_key`, `resource_owner_secret` (pyetrade names)
- Implement custom OAuth handler for E*TRADE specifics
- Always use `https://api.etrade.com` for token endpoints
- Decode tokens with `urllib.parse.unquote()`
- Normalize API responses before parsing
- Cache tokens to avoid re-authentication

❌ **Don't:**
- Use E*TRADE parameter names with pyetrade (`consumer_key` won't work)
- Use pyetrade's built-in OAuth flow without customization
- Use `https://apisb.etrade.com` for token operations
- Assume API responses are always dicts

---

## References

- [E*TRADE API Documentation](https://developer.etrade.com/)
- [pyetrade GitHub](https://github.com/jessecooper/pyetrade)
- [OAuth 1.0a Specification](https://tools.ietf.org/html/rfc5849)