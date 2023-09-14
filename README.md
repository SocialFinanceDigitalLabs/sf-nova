# sf-nova
Create small python apps that run entirely in the browser using stlite and streamlit.

sf-nova uses mainly two libraries:

- [streamlit](https://docs.streamlit.io/) - web applications using simple python code. Check the documentation to learn 
how to write apps.
- [stlite](https://github.com/whitphx/stlite) - allows to use stramlit in the browser (using pyodide). If you're just 
writing apps, you don't have to worry about this.

All you need to do is to write your own streamlit apps and they can be run through sf-nova.

# How to start

Let's go ahead and create, run and publish a small testing app. 

> If you just want to see the final result, check [this python file](/examples/hello_app/app.py) which creates 
[this live app](https://sfdl.org.uk/sf-nova/?url=https://raw.githubusercontent.com/SocialFinanceDigitalLabs/sf-nova/main/examples/hello_app/app.py).


## Create a repository
The first thing you need is a place to store your code. That's called a repository (or repo). In theory, it could be this one (sf-nova) but to avoid having it crowded with multiple apps, we suggest you create your own. If you already have a github repository where you store some code, you can skip this step. If not, you can just follow [this guide](https://docs.github.com/en/get-started/quickstart/create-a-repo).

## Setup the editor


2. In your repository main page open the [web-based editor](https://github.com/github/dev) by pressing the . key on the keyboard.

3. Ensure you have the suggested extensions installed - a popup should open on the lower right side of your screen a 
few seconds after you open this editor. If it doesn't, go to the sidebar of the editor, click on the `extensions` icon 
and check the `recommended` section. You should see a social finance extension called `sf-stlite` (if not, search for
it). Install it.

> :warning: please ensure you have installed the `sf-stlite` extension and not the original `stlite` extension - the latter currently doesn't work while the former is an adaptation written by Social Finance that works properly.

## Create an app
1. Create a new directory for your app (for example, `my_very_first_app`) 
and create your main app python file within it (it can be `my_very_first_app/app.py` or 
`my_very_first_app/my_very_first_app.py` or whatever you want).

2. Let's create a sample app that asks for a username and says hello back to the user. In the file 
`my_very_first_app/app.py` add the following code and save it:

    ```python
    import streamlit as st

    name = st.text_input("What's your name?")

    if name:
        st.write(f'Hello {name}!')
    ```

    In here we:

    - Import the [streamlit](https://docs.streamlit.io/) package
    - ask for the users name with a text input
    - say hello to the user once they submit their name

## Preview the app
1. With your app's python file opened (and focused), click on the `stlite` icon on the sidebar (it should be the one 
bellow the `github` icon) and press "Launch stlite preview". 

    ![Screenshot of stlite Icon](/img/stlite.png) 

2. You can also run it from vscode command palette: `ctrl` + `shift` + `P` and search for the command 
`launch stlite preview`. You should now see a preview on the right side of your editor, while your app's code is in 
your left side:

    ![Screenshot of launching preview](/img/preview_sample.gif)

3. You can now edit the code and, once you save the python file, it will update the app's preview accordingly. If it 
doesn't, edit the settings of your streamlit preview screen (on the top right button) and check the "Run on save" 
option - that will ensure your preview reloads every time you change something in your code (and save the file(s)).

4. If you need to use external libraries (such as `matplotlib` to render charts or `openpyxl` to read excel files) 
ensure that those libraries are listed in a `requirements.txt` file in the same directory as your python file is. 
Check [this example for guidance](/examples/network/requirements.txt). 

## Share the app
5. Once you are happy with your changes, you can commit them to your repository. "commit" just means you are saving your changes. Check [this page](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor#commit-your-changes) for guidance.

6. Finally, you can now share your app. Go to https://sfdl.org.uk/sf-nova and paste the link to your app's code (for example, `https://github.com/SocialFinanceDigitalLabs/sf-nova/tree/main/examples/hello_app`). Follow the instructions on the screen and you should be able to have your app up and running! In this example, the final app page would be this one: https://sfdl.org.uk/sf-nova/?url=https://raw.githubusercontent.com/SocialFinanceDigitalLabs/sf-nova/main/examples/hello_app/app.py.
