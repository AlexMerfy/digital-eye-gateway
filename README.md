# Digital Eye Gateway

Digital Eye Gateway is a Home Assistant app for the Digital Eye Android video-doorbell project.

Version 0.2.0 adds the first functional backend:

- Firebase Admin SDK initialization from `/config/firebase-service-account.json`
- `GET /health` status endpoint
- authenticated `POST /api/test-push` endpoint for FCM test notifications
- ARM64 image for Raspberry Pi 5 / Home Assistant OS
- prebuilt image publication to GHCR

## Home Assistant app configuration

The app uses its private `app_config` directory, mounted inside the container as `/config`.

Place the Firebase service-account key there as:

`/config/firebase-service-account.json`

Never commit that file to this repository.

The API listens on TCP port `8099`.

## API key

Set a strong `api_key` in the Home Assistant app Configuration tab before using the test-push endpoint.

Requests to `POST /api/test-push` must include:

`X-API-Key: <your api_key>`

Example JSON body:

```json
{
  "token": "FCM_DEVICE_TOKEN",
  "title": "Digital Eye",
  "body": "Test notification",
  "data": {
    "event": "test"
  }
}
```

## Health check

`GET /health`

The response reports the app version, whether Firebase credentials loaded successfully, and whether an API key is configured. It never returns credentials or the API key.

## Image

`ghcr.io/alexmerfy/digital-eye-gateway:0.2.0`

The workflow also publishes `latest`.

## Security

Do not commit Firebase credentials, Home Assistant tokens, camera credentials, API keys, or other secrets.
