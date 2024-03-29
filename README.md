# Che Mondis - Weather API

## Overview

This project deploys a Django REST API enabling users to fetch the current weather in any city. The data is pulled from [Open Weather Map](https://openweathermap.org). Results are [cached](#caching) for a configurable amount of time, to avoid hitting the upstream API too often.

In this document:

- [Usage](#usage)
  - [Query Parameters](#query-parameters)
- [Development/Local Deployment](#development)
  - [Requirements](#requirements)
  - [Steps](#steps)
  - [Configuration](#configuration)
- [Caching](#caching)

## Usage

The API can be quickly accessed at the live endpoint: `https://chemondis-weather-api-rt645.ondigitalocean.app/weather/{city}`, where `{city}` is the name of the city you want to fetch the weather for.

> [!TIP]
> Using the Open API spec found at [/docs/openapi.json](https://github.com/SkepticMystic/chemondis-weather-api/blob/main/docs/openapi.json), you can execute the API directly from the documentation page. Paste the file contents into the editor at [editor.swagger.io](https://editor.swagger.io), and click the "Try it out" button.
> The spec can call the endpoint from the live URL on Digital Ocean, or on a [locally deployed](#development) instance (`http://localhost:8000`).

The result is returned as a JSON object.
On a successful request, the response will be in the following shape (the `Weather` type is defined further below):

```ts
{
  ok: true,
  data: Weather
}
```

On an unsuccessful request, the response will indicate an error occured, with a string message:

```ts
{
  ok: false,
  data: string
}
```

Therefore, the general shape of a response is a [tagged union](https://en.wikipedia.org/wiki/Tagged_union). The consumer of the API can check the `ok` property to determine if the request was successful or not.

The `Weather` type is defined as follows:

```ts
{
  city: string,
  temp: number,
  temp_min: number,
  temp_max: number,
  humidity: number,
  pressure: number,
  wind_speed: number,
  wind_direction: "north" | "south" | "east" | "west",
  description: string,
  timestamp: string
}
```

### Query Parameters

The following query parameters can be used to customize the response:

- `lang`: The language to return the weather description in. Defaults to `en`. Supported values are:
  - `en` (English 🇬🇧)
  - `de` (German 🇩🇪)
  - `af` (Afrikaans 🇿🇦)

## Development

The project can also be built and run locally.

### Requirements

- Docker
- An OpenWeatherMap API key
  - You can get one for free [here](https://openweathermap.org/api).

### Steps

To deploy the API in your local environment, follow these steps:

1. Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/SkepticMystic/chemondis-weather-api.git
cd chemondis-weather-api
```

2. Create a `.env` file in the root of the project, and set the `OPEN_WEATHER_API_KEY` variable to your [OpenWeatherMap API key](#requirements). The file should look like this (with `{your-api-key}` replaced with your actual API key):

```env
OPEN_WEATHER_API_KEY="{your-api-key}"
```

3. Build and run the Docker container:

```sh
docker compose up --build
```

The API should now be running at `http://localhost:8000`.

### Configuration

The following environment variables can be set to configure the API. They can be set in a `.env` file in the root of the project.

- `CACHE_TTL_MINS`: The time-to-live (TTL) for cache items, in minutes. Defaults to 5 minutes. Valid values are: `5`, `10`, and `60`. Invalid values will be ignored, and the default will be used.

## Caching

Responses from OpenWeatherMap are cached on two levels:

1. All responses are stored in SQLite, and only retrieved if still fresh.
2. In the browser, using the Cache-Control header.

These two approaches work together to reduce the total number of requests to the upstream API, while still providing fresh data to the user. Individual users making the same request will receive the browser-cached response, while different users querying the same city will receive each other's cached responses from the database.
