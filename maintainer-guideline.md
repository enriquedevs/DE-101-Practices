# Maintainer Guideline

## Markdown guidelines

* Follow the linter on: `DavidAnson.vscode-markdownlint` VSCode extension
* Additionally, for consistency:
  * Unordered lists must be launched by using asterisc '*'

    ```md
    * First element
      * First child
    ```

  * Code blocks must have the extension of the file instead of the file type, if not sure what extension is, use txt

    ```md
    Use:
    ```sh
    print 'Hello world'
    
    Instead of
    ```shell
    print 'Hello world'
    ```

  * Links should be always the last section of the document
    * All links should be linked in the bottom of the document, wrapped by `## Links`
    * All links reference should be at the bottom of the document for reference
  * The main document should always be named `README.md`, with uppercase
  * Additional markdown documents should be `kebab-case`
    * Ex. use `pre-setup.md` instead of `pre_setup.md`
  * Use 2 spaces tab as separator
  * All image and local links files must be on linux style using `./<relative path>` or `../<relative path>`

## Folder structure

* Inside the `Practices` folder the files meet the following criteria
  * All folders must be `snake_case`
  * All folder must follow the name `session_<session number>_<topic in snake_case>`
    * The topic must be a max of 3 lowercase words
  * Each lesson folder can contain up to 3 files and 1 folder
    * `README.md`
    * `img` \
      This folder will contain all images to be used in markdown documents
    * `pre-setup.md` (Optional) \
      This contain a pre-setup instructions for the session
    * `practice_files` \
      This folder will contain any additional file required for the practice
    * `admin notes` \
      This file will contain some notes for the instructor, such as policies setups...

### Subfolders

* Files inside `img` will follow the `kebab-case` naming, they can be `png`, `jpg` or `gif`
* Files inside `practice_files` may or may not follow the casing rules, this depends on the practice contents and the writers preference, however, ensure the casing is consistent for that folder.
  * It does not need to match other folders style, just be consistent with itself.

## README.md

* Each session must contain the following sections
  * `# <Session name>` \
    The session name must match the one in Canvas and in Kick off ppt
  * `## Prerequisites` (Optional) \
    Mention the pre-setup
  * `## Before start` (Optional) \
    If any concept is required to reinforce that was seeing during the pre-setup mention it here
  * `## What You Will Learn` \
    Described in a short list
  * `## Practice` \
    Described briefly the goal
    >All theory content must be placed here or in any of the children subsections
  * `### Requirements` \
    Specific requirements list to achieve the goal described above
    * Link the pre-setup if any
    * Credentials + other non installers
    * All the installers must be in the pre-setup document \
      Specific setup for the installers can be mentioned here, such as connections test for databases...
  * `### Step <Number> - <Step name>` \
    Develop the step
    * Avoid developing the step in the step name: \
      Ex. use: `### Step 1 - Docker` instead of `### Step 1 - Create the dockerfile`
      >Use as many steps as required
  * `## Homework` (Optional) \
    Described in a short list
  * `## Conclusion` (Optional) \
    Described in 1 or 2 short paragraphs
    >When there is no theory content this is optional
  * `## Still curious` \
    Use this section to explain related topics that may help the student with interviews, where to improve on skill/technology knowledge for the current topic...
  * `## Links`
    This section will contain all links used during the document \
    Ex.
    * During the document `...check this [article][article_link] for more information..`
    * Links section:
      * `* [More information article][article_link]`
      * `[article_link]: https://articlesite.com`
    * You can use blank lines to separate links definition groups as this does not affect the final output\
      Ex. Blank space to separate local file links from web links:

      ```md
      [pre-setup]: ./pre-setup.md

      [csv]: ./practice_files/clinic.csv
      [sql_conventions]: https://www.sqlshack.com/learn-sql-naming-conventions/
      ```

Template: [Session template][template_readme]

## pre-setup.md

* Each pre-setup must contain the following sections
  * `# Pre-setup`
  * `## Prerequisites` (Optional) \
    List of requirements with their links to install...
  * `## Steps` \
    This section is just a wrapper for all the steps
  * `### Step <Number> - <Step name>`
  * `## Links` \
    This section will contain all links used during the document \
    Ex.
    * During the document `...check this [article][article_link] for more information..`
    * Links section:
      * `* [More information article][article_link]`
      * `[article_link]: https://articlesite.com`

>Pre-setup will not contain theory information, it may contain some brief explaining parameter commands or similar quick reference items, but any relevant concept must be explained in the same folder `README.md` in the section `## Before Start`

Template: [pre-setup][template_pre]

## Links

* [Session template][template_readme]
* [Pre-setup template][template_pre]

[template_readme]: ./template-readme.md
[template_pre]: ./template-pre-setup.md
