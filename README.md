# Che Mondis - Weather API

## Overview

This project deploys a Django REST API enabling users to fetch the current weather in any city. The data is pulled from [Open Weather Map](https://openweathermap.org). Results are cached for a configurable amount of time, to avoid hitting the upstream API too often.

## Requirements

- Docker
- An OpenWeatherMap API key
  - You can get one for free [here](https://openweathermap.org/api).

## Deployment

To deploy the API in your local environment, follow these steps:

1. Clone the repository:

```sh
git clone https://github.com/SkepticMystic/chemondis-weather-api.git
```

2. Navigate to the project directory:

```sh
cd chemondis-weather-api
```

3. Create a `.env` file in the root of the project, and set the `OPEN_WEATHER_API_KEY` variable to your [OpenWeatherMap API key](#requirements). The file should look like this (with `{your-api-key}` replaced with your actual API key):

```env
OPEN_WEATHER_API_KEY="{your-api-key}"
```

4. Build and run the Docker container:

```sh
docker compose up --build
```

## Usage

Once running, the API can be accessed at `http://localhost:8000/weather/{city}`, where `{city}` is the name of the city you want to fetch the weather for.

> [!TIP]
> Using the Open API spec found at [/docs/openapi.json](https://github.com/SkepticMystic/chemondis-weather-api/blob/main/docs/openapi.json), you can execute the API directly from the documentation page. Paste the file contents into the editor at [editor.swagger.io](https://editor.swagger.io), and click the "Try it out" button.

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

Therefore, the general shape of a response is a [discriminated union](https://en.wikipedia.org/wiki/Tagged_union). The consumer of the API can check the `ok` property to determine if the request was successful or not.

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
  - `en` (English)
  - `de` (German)
  - `af` (Afrikaans)

## Configuration

The following environment variables can be set to configure the API. They can be set in a `.env` file in the root of the project.

- `CACHE_TTL_MINS`: The time-to-live (TTL) for the cache, in minutes. Defaults to 5 minutes.
