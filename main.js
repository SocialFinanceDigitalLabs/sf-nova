const BASE_APP_FILES = {
  "sf-nova.py": {
    url: "https://raw.githubusercontent.com/SocialFinanceDigitalLabs/sf-nova/main/sf-nova.py",
  },
};

function urlsToObject(urls, prefix = "") {
  return urls.reduce((acc, url) => {
    const fileName = url.split("/").pop();
    acc[`${prefix}${fileName}`] = { url };
    return acc;
  }, {});
}

const BASE_REQUIREMENTS = ["streamlit_javascript"];
const loadAppFromUrl = () => {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  const files = urlsToObject(urlParams.getAll("file"));
  const pages = urlsToObject(urlParams.getAll("page"), (prefix = "pages/"));

  const requirements = urlParams.getAll("req");
  if (Object.keys(files).length === 0) {
    mountStlite(BASE_APP_FILES, BASE_REQUIREMENTS);
    return;
  }

  mountStlite({ ...files, ...pages }, requirements);
};

const mountStlite = (files, requirements) => {
  console.log(files);
  console.log(requirements);
  const entryPointName = Object.keys(files)[0];
  stlite.mount(
    {
      requirements: requirements, // Packages to install
      entrypoint: entryPointName, // The target file of the `streamlit run` command - use the first file present
      files: files,
    },
    document.getElementById("root")
  );
};

loadAppFromUrl();
