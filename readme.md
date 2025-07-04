# Mark's JAMStack Prayer Site

I use this site for daily prayer.  I have secured it with my Microsoft account via Azure Active Directory and use Contentful for the content.  

Here is what I have so far:  

- Created the site using the [Hugo](https://gohugo.io/) static site generator.
- Set up the site with the [Jane theme](https://github.com/xianmin/hugo-theme-jane).  
  - Note that [Hugo Themes on Netlify](https://docs.netlify.com/configure-builds/common-configurations/hugo/#hugo-themes) should be installed as a git submodule.
    - cd YOUR_PROJECT_DIRECTORY:

    ```bash
    git init #if you haven't already
    git submodule add https://github.com/THEME_CREATOR/THEME_NAME
    # Instead of `git submodule add` above, what I did per theme repo readme: git clone https://github.com/xianmin/hugo-theme-jane.git --depth=1 themes/jane
    git submodule update
    ```

- Set up the site on the [Netlify](https://www.netlify.com/) CMS as [Mark's JAMStack Prayer Site](https://m2prayer.netlify.app/)
- Removed the [Mark's JAMStack Prayer Site](https://m2prayer.netlify.app/) from the [Netlify](https://www.netlify.com/) as password protecting the site was a paid service.
- Set up a free [Azure Static Web App](https://witty-grass-042828710.1.azurestaticapps.net/) with free hosting.
- Set up password protection for the Azure Static Web App per the staticwebapp.config.json file:

```javascript
{
    "routes": [
        {
            "route": "/prayer*",
            "allowedRoles": ["authenticated"]
        }
    ],
    "responseOverrides": {
        "401": {
          "statusCode": 302,
          "redirect": "/.auth/login/aad"
        },
        "403": {
          "redirect": "/.auth/login/aad"
        },
        "404": {
          "redirect": "/404.html"
        }
      }
}
```

- As you can see above, the /prayer* route is protected by the Azure Static Web App.  If a 401 is returned, the user is redirected to the Azure login page (Azure Active Directory).  If a 403 is returned, the user is redirected to the Azure login page.  If a 404 is returned, the user is redirected to the 404.html page.  

- Set up contentful-hugo doing the following from the CLI:

```bash
npm install contentful-hugo
```

- Create the Javascript Config:  

```javascript
// contentful-hugo.config.js

module.exports = {

    contentful: {
        // defaults to CONTENTFUL_SPACE env variable
        space: 'space-id',
        // defaults to CONTENTFUL_TOKEN env variable
        token: 'content-deliver-token',
        // defaults to CONTENTFUL_PREVIEW_TOKEN env variable
        previewToken: 'content-preview-token',
        // defaults to "master"
        environment: 'master',
    },

    singleTypes: [
        {
            id: 'homepage',
            directory: 'content',
            fileName: '_index',
        },
        {
            id: 'siteSettings',
            directory: 'data',
            fileName: 'settings',
            fileExtension: 'yaml', // default is md
        },
    ],

    repeatableTypes: [
        {
            id: 'posts',
            directory: 'content/posts',
            mainContent: 'content',
            resolveEntries: {
                categories: 'fields.slug',
                author: 'fields.name',
                relatedPosts: 'sys.id',
            },
        },
        {
            id: 'seoFields',
            isHeadless: true,
            directory: 'content/seo-fields',
            customFields: {
                // these fields will be added to the frontmatter
                myCustomField: 'myCustomFieldVal',
                myOtherCustomField: (entry) => {
                    return entry.fields.whatever;
                },
            },
        },
        {
            id: 'reviews',
            directory: 'content/reviews',
            mainContent: 'reviewBody',
        },
        {
            id: 'category',
            directory: 'content/categories',
            isTaxonomy: true,
        },
    ],

    staticContent: [
        {
            inputDir: 'static_content',
            outputDir: 'content',
        },
    ],
};
```

To use contentful-hugo to generate data from the Contentful:

```bash
npx contentful-hugo [flags]
```

Here is what I ran:  

```bash
npx contentful-hugo --wait 2000 --preview --config contentful-hugo.config.js
```

Here are the flags that can be used:

| flag      | aliases | description                                                                                              |
| --------- | ------- | -------------------------------------------------------------------------------------------------------- |
| --init    |         | Initialize the directory. Generates a config file and default shortcodes for Contentful rich text fields |
| --preview | -P      | Runs in preview mode, which pulls both published and unpublished entries from Contentful                 |
| --wait    | -W      | Wait for the specified number of milliseconds before pulling data from Contentful.                       |
| --config  | -C      | Specify the path to a config file.                                                                       |
| --server  | -S      | Run in server mode to receive webhooks from Contentful                                                   |
| --port    |         | Specify port for server mode (Default 1414)                                                              |
| --clean   |         | Delete any directories specified in singleTypes and repeatableTypes                                      |
| --help    |         | Show help                                                                                                |
| --version |         | Show version number                                                                                      |
  
So, the command that I used does the following. Wait 2000 milliseconds (2 seconds) before pulling data from Contentful, run in preview mode (which pulls both published and unpublished entries from Contentful), and specify the path to a config file.  

- Set up a Hugo shortcodes in `layouts\shortcodes\requests.html` and updated prayer.md content directory to display the data from the contentful-hugo run.  

Then, I had issues with the Azure build in GitHub Actions:  

```bash
Detecting platforms...
Detected following platforms:
  nodejs: 14.18.3
  hugo: 0.81.0
Version '14.18.3' of platform 'nodejs' is not installed. Generating script to install it...
Error: Could not find either 'build' or 'build:azure' node under 'scripts' in package.json. Could not find value for custom run build command using the environment variable key 'RUN_BUILD_COMMAND'.Could not find tools for building monorepos, no 'lerna.json' or 'lage.config.js' files found.


---End of Oryx build logs---
Oryx could not find a 'build' or 'build:azure' script in the package configuration. Please add one of these commands to your package configuration file (i.e. package.json). Alternatively, you can add the app_build_command to the build/deploy section of your workflow file. For example, app_build_command: 'npm run docs:build'

For further information, please visit the Azure Static Web Apps documentation at https://docs.microsoft.com/en-us/azure/static-web-apps/
If you believe this behavior is unexpected, please raise a GitHub issue at https://github.com/azure/static-web-apps/issues/
Exiting
```

Note that you should not track package-lock.json or package.json as they cause an issue with the Azure Static build GitHub Action. The package-lock.json file is used by the Azure Static build GitHub Action to install nodejs dependencies and causing a build failure. However, apparently the package.json file is also used by the Azure Static build GitHub Action to install nodejs dependencies and causing a build failure. Here is the error message in the Azure Static build GitHub Action Build and Deploy Job output

```bash
Error: Could not find either 'build' or 'build:azure' node under 'scripts' in package.json. Could not find value for custom run build command using the environment variable key 'RUN_BUILD_COMMAND'.Could not find tools for building monorepos, no 'lerna.json' or 'lage.config.js' files found.


---End of Oryx build logs---
Oryx could not find a 'build' or 'build:azure' script in the package configuration. Please add one of these commands to your package configuration file (i.e. package.json). Alternatively, you can add the app_build_command to the build/deploy section of your workflow file. For example, app_build_command: 'npm run docs:build'
```

After removing the package-lock.json and package.json files, the build worked.

## Azure Static Web App Portal Settings

Here are the screenshots of the Azure Static App settings on the Azure Portal.

### Azure Static Web App Hosting Plan Settings

![Azure Hosting Plan](readmeImages/AzureHostingPlan.png)

### Azure Static Web App Environment Settings

![Azure Environments](readmeImages/AzureEnvironments.png)

### Azure Static Web App Role Settings

![Azure Static Web App Role Settings](readmeImages/AzureRoleSettings.png)

## Current GitHub Action YML File

```yaml
name: jamstack-azure-static-web-app-ci-cd

on:
  push:
    branches:
      - main
  repository_dispatch:
    types: [start-workflow]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main
  schedule:
    # Run every day at 4:00 AM. Use https://crontab.guru/ to set the correct time.
    - cron: '0 9 * * *'

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed') || github.event_name == 'repository_dispatch' || github.event_name == 'schedule'
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v2
        with:
          submodules: true
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_WITTY_GRASS_042828710 }}
          repo_token: ${{ secrets.GITHUB_TOKEN }} # Used for Github integrations (i.e. PR comments)
          action: "upload"
          ###### Repository/Build Configurations - These values can be configured to match your app requirements. ######
          # For more information regarding Static Web App workflow configurations, please visit: https://aka.ms/swaworkflowconfig
          app_location: "/" # App source code path
          api_location: "" # Api source code path - optional
          output_location: "public" # Built app content directory - optional
          ###### End of Repository/Build Configurations ######

  close_pull_request_job:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request Job
    steps:
      - name: Close Pull Request
        id: closepullrequest
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_WITTY_GRASS_042828710 }}
          action: "close"

```

## Scripts

I have created a scripts folder off the root of the repository. This folder contains the following scripts:
| Name | Description |
| ---- | ----------- |
| contentful-hugo.config.js | Script to pull data from Contentful using the contentful-hugo npm package. |
| daily-verse.js | Node script to pull daily verse data from my API in Heroku. |
| esv-verse.js | Node script to pull ESV verse data from my ESV API. |
| memoryverses.js | Node script to pull memory verse data from my API in Heroku. |
| staff.js | Node script to pull staff data from my API in Heroku. |
| update-esv-json.js | Node script to to pull staff data from my API in Heroku. |
| wsc.js | Node script to pull Westminster Shorter Catechism data from my API in Heroku. |
| prayer-requests.js | Node script to pull prayer request data from my API in Heroku. |  
| countries.js | Node script to pull country data from my API in Heroku. |

I use the above scripts to update the JSON files in the `data` folder.  

## Shortcodes

I have created a `layouts/shortcodes` folder off the root of the repository. This folder contains the following shortcodes:
| Name | Description |
| ---- | ----------- |
| memory-verse.html | Shortcode to display today's memory verse. |
| requests.html | Shortcode to display today's prayer requests obtained from Contentful. |
| the-date.html | Shortcode to display the current date. |
| todays-staff.html | Shortcode to display today's staff for which to pray. Also provides a mailto link. |
| todays-verse.html | Shortcode to display today's verse. |
| todays-wsc.html | Shortcode to display today's Westminster Shorter Catechism Q/A. |
| prayer-requests.html | Shortcode to display today's prayer requests. |
| category-menu.html | Shortcode to display a drop down HTML select menu of prayer categories. |
| mission-links.html | Shortcode to display the week's mission link. |
| todays-country.html | Shortcode to display today's country link to the Prayer Cast website. |
| todays-psalm.html | Shortcode to display today's psalm. |

## Conventional Commits

Conventional commits are a way to make your code more readable and maintainable. I added the VS Code extension [Conventional Commits](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits) to my local VS Code. This extension should help me be more consistent with my commits. The [URL](https://conventionalcommits.org/) for conventional commits is a great resource.
