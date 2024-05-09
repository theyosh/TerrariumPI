---
title: Unsplash background
categories: [Website, FAQ]
tags: [unsplash, background]
---

Create a [free account](https://unsplash.com/join) at Unsplash.

After that, you need to [create an app](https://unsplash.com/oauth/applications/new) in Unsplash. Check all the boxes and accept the terms.

![Unsplash create application](/assets/img/UnsplashApp.webp){: .center }

You will get a popup asking for the application name. Enter TerrariumPI. The description field is not needed.

On the next page you will see your created application. Scroll down to the section **Keys**.

![Unsplash access keys](/assets/img/UnsplashAccessKey.webp){: .center }

Copy the value of the **Access Key** field. This value is needed at the settings page.

Now go to your TerrariumPI [settings]({% link _tabs/setup.md %}#Unsplash) page, and enter the Access Key value here at the Cloud part of the settings screen.
The access will be stored encrypted in the database.

The second field at the settings page allows to specify the keyword(s) to use to get a new background image.

Now when the web GUI interface is loading, a random background image will be loaded.
