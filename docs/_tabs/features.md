---
title: Features
icon: fas fa-info
order: 2

image:
  path: /assets/img/options.webp
  src: /assets/img/options.webp
  alt: Feature header image
---
Here are some features that TerrariumPI has.

## Local weather and climate mirroring

Using local weather data, you can use sunrise and sunset as timers for your lights or other relays. This way you get automatically seasons following the season outside. [More...]({% link _tabs/setup.md %}#weather)

It is also possible to mirror the temperature and humidity of the weather at the given location. This can be set on every temperature or humidity controlled area. And per area you can even select an offset, so you can create shade area and a full sun area based on the same climate. Look at the variation tab to set this up.

But you can even enter an external JSON source for climate mirroring. Look [How to use remote data FAQ]({% link _faq/remote_data.md %}) how to add the correct url.

## Multilingual

The software is translated to multiple languages. This will also select the correct currency, number and date formatting. If you language is not available or is not complete, go to the [translation page]({% link _tabs/translations.md %}) to see how to update it.

## Multiple enclosures and multi areas

It is possible to control multiple enclosures with a single Raspberry PI. As long you can hook up enough sensors and relays, you can create unlimited enclosures and areas.

In every enclosure you can create multiple areas, even of the same type, to setup your enclosure. So you can create a sun spot area and a shading spot area that have their own settings and logic in the same enclosure.

## Data encryption

Some data is sensitive like the authentication password or the cloud credentials. This data is stored encrypted in the TerrariumPI database. That means when you database is lost, your passwords will not be compromised directly.

There is a difference in how the data is encrypted.

### Admin password

The admin password is encrypted one way in a hash, and that hash is checked with the entered login credentials. This password cannot be reverted back to plain text if you loose it. [But you can reset it]({% link _faq/reset_authentication.md %})

For encryption we use [bcrypt](https://en.wikipedia.org/wiki/Bcrypt).

### Other sensitive data

Cloud credentials are stored with symmetric encryption. This means that the data can be reverted back to plain text. This is needed to able to login to the cloud providers. TerrariumPI is logging as 'you'.

For encryption we use [Fernet](https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet) encryption with the CPU serial as salt. As every CPU has it's own serial, the salt is unique and locked to your Raspberry PI.

## Docker

You can also install a Docker image to make the installation easier. More information can be found at [installation page]({% link _tabs/install.md %}#docker)
