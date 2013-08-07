# Zoopla API for Python

Note that we don't currently support the full API.

Please refer to the [Zoopla API documentation](http://developer.zoopla.com/docs)

```python
import zoopla
api = zoopla.Api(version=1)

for listing in api.property_listings(
        area='Liverpool',
        property_type='houses',
        max_results=None):
    
    print("outcode: {}, short_description: {}".format(
        listing.outcode,
        listing.short_description))
```
