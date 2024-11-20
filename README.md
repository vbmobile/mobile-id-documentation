# mobile-id-documentation
This repo contains documentation regarding our MobileID SDK for both Android and iOS with sample applications

# MobileID SDK Documentation

This repo will be used to store mkdocs project.

## Commands

- mkdocs build - Generate a folder "site" with the static content of the current markdown files and assets.
- mkdocs serve - Creates a local server that automatic renders the changes in markdown files to help in development mode.

Mike plugin offers the following commands to test, publish and manage versioning:

- mike list - Lists all the versions that are available in this project
- mike delete <version_name> - deletes the version name from the list of versions
- mike serve - starts localhost server
- mike deploy --push <version_name> - Deploys a new version from current branch with the name passed in the command
- mike deploy --push --update-aliases <version_name> latest - Deploys a new version and tags it as latest

Release that has the tag latest will be used automatically. 
Also when a user is viewing any other version that is not the latest, 
a banner will appear showing a warning that a new version is available.

## Website Structure

Currently we have 4 main tabs in the website:
- Getting Started - Landing page with generic information regarding our SDK
- Features - Contains a submenu with every feature that our SDK offers
- Release Notes - Contains our release notes information
- Migration Guide - Contains our migration guide information

## Project Structure
MKDocs uses an YML file for configuration that can be found in the root folder.
In the gitignore should be everything else (IDE files, generated website from command) to keep the repo clean.
All the markdown files and assets have to be inside the docs folder.
Inside the docs folder we have the following structure:
- Assets - Contains general assets (Logo, css files etc..) to use in the website.
- Features:
    - Biometric Match - Contains markdown files and assets related to Biometric Match.
    - Boarding Pass - Contains markdown files and assets related to Boarding Pass.
    - Document Reader - Contains markdown files and assets related to Document Reader.
    - Face Capture - Contains markdown files and assets related to Face Capture.
    - Subject Management - Contains markdown files and assets related to Subject Management.
- Release Notes - Contains markdown files and assets related to release notes.
- Migration Guide - Contains markdown files and assets related to migration guide.


## Tools Helper

### mkdocs
https://squidfunk.github.io/mkdocs-material/

### Mike cmd 
Install from oficial repo: https://github.com/jimporter/mike