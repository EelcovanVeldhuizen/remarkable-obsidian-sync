<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/EelcovanVeldhuizen/remarkable-obsidian-sync">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Remarkable to Obsidian Sync</h3>

  <p align="center">
    This project syncs but mostly converts your remarkable drawings to Excalidraw / markdown files that can be used in combination with the [Obsidian Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin).
    <br />
    <br />
  
    <a href="https://github.com/EelcovanVeldhuizen/remarkable-obsidian-sync/issues">Report Bug</a>
    ·
    <a href="https://github.com/EelcovanVeldhuizen/remarkable-obsidian-sync/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

The usage is pretty straight forward. There are some dependencies, see the Dockerfile if you want to know more.


### Prerequisites

You need to have Docker if you want use this script the same way as I do. How to get Docker is explained [on the Docker website](https://docs.docker.com/get-docker/).

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._


1. Make sure you have something to copy the files from the remarkable to your machine. I use Rsync which comes with MacOs and almost every Linux distribution.

2. Clone the repo
   ```sh
   git clone git@github.com:EelcovanVeldhuizen/remarkable-obsidian-sync.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Sync your remarkables with RSYNC (or any other tool). This works the best if you have set-up passwordless login with the help of SSH keys. The best explenation how to do this I found this [Reddit Post](https://www.reddit.com/r/RemarkableTablet/comments/78u90n/passwordless_ssh_setup_for_remarkable_tablet/).


```sh
rsync -av root@10.11.99.1:/home/root/.local/share/remarkable/xochitl/ <path_to_remarkables>
```

I use Docker to create keep the python installtion on my machine clean.

To build build the container (which will be named ros):

```sh
docker build -t ros .
```

Run the container with the paths to your remarkable files and where you want the markdown files to end up.

```sh
docker run  -v <path_to_remarkables>:/app/remarkables:ro -v <path_to_dir_in_vault>:/app/vault ros
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
You can reach me on Github!

Project Link: [https://github.com/EelcovanVeldhuizen/remarkable-obsidian-sync](https://github.com/EelcovanVeldhuizen/remarkable-obsidian-sync)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [RMScene by Ricklupton](https://github.com/ricklupton/rmscene)
* [RMC by Ricklupton](https://github.com/ricklupton/rmc)
* [Best README Template by Othneildrew](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>