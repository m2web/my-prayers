# Mark's Private Prayer Site

I use this site for daily prayer.  

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
- Removed the [Mark's JAMStack Prayer Site](https://m2prayer.netlify.app/) from the [Netlify](https://www.netlify.com/) as password protecting the site was a paid service. I have also removed it from Azure Static Web App.
- Now using Cloudflare Pages to host the site.



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





## Current GitHub Action YML File

```yaml
name: github pages


  push:
    branches:
      - main  # Set a branch to deploy
  pull_request:
  schedule:
    # Run every day at 4:00 AM. Use https://crontab.guru/ to set the correct time.
    - cron: '0 9 * * *'  

## Scripts
  deploy:
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.121.1'
          extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public

```

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

