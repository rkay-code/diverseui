# Diverse UI

Diverse UI is a free collection of diverse user-submitted images that can be used in your design work.

This is a repository of the code that powers both the website and the API.

## API

````
GET /images
````

With the following parameters:

| Parameter | Type   | Required? | Description |
|-----------|--------|-----------|-------------|
| `gender`  | string | optional  | The gender of the images. We currently only support `male` or `female`. By default, we return all genders. |
| `count`   | number | optional  | The number of images. By default, we return all the images. |

The response is a array of objects each with an image URL and gender. Example response:

````
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "gender": "female",
    "url": "https://d3iw72m71ie81c.cloudfront.net/female-34.jpg"
  },
  {
    "gender": "male",
    "url": "https://d3iw72m71ie81c.cloudfront.net/male-4.jpg"
  }
]
````

## Contributors

* [Yefim Vedernikoff](https://twitter.com/yefim)

* [Renee Padgham](https://medium.com/@reneepadgham)
