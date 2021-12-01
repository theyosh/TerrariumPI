# Update documentation

In order to update or add new documentation you need to have Jekyll installed. Then fork this repository and checkout the `4.x.y.z` branch. From that, make a new branch to make your changes. Then create a pull request for the `4.x.y.z` branch. When the pull request is finished, a new version of the documentation will be created at https://theyosh.github.io/TerrariumPI

This can be done on a normal computer/laptop. The documentation does not need a running TerrariumPI.

The documentation is created using Jekyll. This is a framework for generating a static website. The pages consists of HTML or Markdown content. More information about Jekyll can be found [here](https://jekyllrb.com/docs/)

## Install Jekyll

Go to https://jekyllrb.com/docs/installation/ and follow the installation instructions.

Then go to the root folder of TerrariumPI and run: `bundle install`. This will install all the needed plugins and template for generating the documentation.

## Run local version

After Jekyll is installed, go to the `docs` folder and run the command `jekyll serve` to open the website at: http://localhost:4000/TerrariumPI/

### Bug
Somehow auto reloading does not work, It produces an error. So you have to manually stop and start again to see the changes.

