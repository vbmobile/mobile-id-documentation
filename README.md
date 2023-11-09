# mobile-id-documentation
This repo contains documentation regarding our MobileID SDK for both Android and iOS with sample applications

# MobileID SDK Documentation

This repo will be used to store mkdocs project.

## Commands

- mkdocs build - Generate a folder "site" with the static content of the current markdown files and assets.
- mkdocs serve - Creates a local server that automatic renders the changes in markdown files to help in development mode.

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