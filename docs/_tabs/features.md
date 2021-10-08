---
title: Features
icon: fas fa-info
order: 2
---
Here are some features that TerrariumPI has.

## Data encryption
Some data is sensitive like the authentication password or the cloud credentials. This data is stored encrypted in the TerrariumPI database. That means when you database is lost, your passwords will not be comprimised directly.

There is a difference in how the data is encrypted.

### Admin password
The admin password is encrypted one way in a hash, and that hash is checked with the entered login credentials. This password cannot be reverted back to plain text if you loose it. [But you can reset it]({{ 'faq/reset_authentication/' | relative_url}})

For encryption we use [bcrypt](https://en.wikipedia.org/wiki/Bcrypt).

### Other sensitive data
Cloud credentials are stored with symmetric encryption. This means that the data can be reverted back to plain text. This is needed to able to login to the cloud providers. TerrariumPI is logging as 'you'.

For encryption we use [Fernet](https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet) encryption with the CPU serial as salt. As every CPU has it's own serial, the salt is unique and locked to your Raspberry PI.

## Local weather
Using local weather data, you can use sunrise and sunset as timers for your lights or other relays. This way you get automatically seasons following the season outside. [More...]({{ 'setup/' | relative_url}}#weather)

## Multilanguage


## Multiple enclosures