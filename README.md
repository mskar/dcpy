# Jupyter Notebook Workflows with Jupytext and Papermill
![](https://raw.githubusercontent.com/mwouts/jupytext/master/docs/logo_large.png)
![](https://media.githubusercontent.com/media/nteract/logos/master/nteract_papermill/exports/images/png/papermill_logo_wide.png)

## Future Meetup

[Data in Government (DiG) Panel
Discussion](https://www.meetup.com/Data-Community-DC/events/278159920)

## Tools

- https://github.com/mwouts/jupytext
- https://github.com/nteract/papermill
- https://github.com/jupyter/nbdime
- https://github.com/fastai/nbdev
- https://mybinder.org/

## Jupyter Notebook Pros and Cons

Pros:
- Intuitive interface
- Ubiquitous (DataBricks, Colab, Azure notebooks, etc.)
- Literate Programming
- Many output formats, including HTML slides

Cons:
- Need to be rendered
- Underlying structure is JSON
- Not great for version control / text editors
- Not like scripts (Harder to test and automate)

## About me

- Site: https://mskar.github.io/
- Twitter: https://twitter.com/marskar
- LinkedIn: https://www.linkedin.com/in/mskar
- Repo: https://github.com/mskar/dcpy

![](https://mskar.github.io/image/martin.png)

## Jupytext

[Repo](https://github.com/mwouts/jupytext)

- Round-trip conversion for Jupyter notebooks
- Many file formats including:
  - [Jupytext Markdown format](docs/formats.md#jupytext-markdown)
  - [MyST Markdown format](docs/formats.md#myst-markdown)
  - [R Markdown format](docs/formats.md#r-markdown)
  - Scripts in [many languages](docs/languages.md)
- Demo files: https://github.com/mwouts/jupytext/tree/master/demo

## Papermill [Repo](https://github.com/nteract/papermill#)
-   **parameterize** notebooks using shell arguments
-   **execute** notebooks like scripts
