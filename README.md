<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/IfanSnek/PyScratch">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">PyScratch</h3>

  <p align="center">
    A framework for creating scratch blocks and projects with python.
    <br />
    <a href="https://pyscratch.readthedocs.io/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://scratch.mit.edu/projects/editor/">Scratch Home Page</a>
    ·
    <a href="https://github.com/IfanSnek/PyScratch/issues">Report Bug</a>
    ·
    <a href="https://github.com/IfanSnek/PyScratch/issues">Request Feature</a>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

### Built With

* [Python](https://www.python.org/)
* [Lark](https://github.com/lark-parser/lark)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

PyScratch is easy to get up and running!

### Installation with Pip

1. pip
  ```sh
  pip install scratch-python
  ```
2. Copy the latest build environment from [releases](https://github.com/IfanSnek/PyScratch/releases) and unzip.

3. Navigate to the build environment
   ```sh
   cd Project
   ```

### Installation from Source

1. Clone the Repo
   ```sh
   git clone https://github.com/IfanSnek/PyScratch.git
   ```
2. Navigate to the installation directory
   ```sh
   cd PyScratch
   ```
3. Install the package
   ```sh
   python setup.py install
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

Here is basic usage for the ScratchText language.

```text
// Currently, there is only support for single line comments

// Import the other file
include module.st

// USe a function from the other file
back walk (10) steps

// Start a new stack
when green flag pressed

// Variables can be set like this. Note that any parameter must be surrounded by parenthesis.
set (health) to (10)

// Blocks are typed as they are seen in Scratch
move (10) steps // Just remember to use parentheses for values.

// You can also put variable randomly. They will start at 0.
move (health) steps

// You can even call an undefined variable and it will start at 0
move (my variable) steps // Note that the parser ignores spaces, so the variable will become 'myvariable'

// Loops are made with brackets
repeat (2) {
    // Indentation is not required but it is good for visibility.
    turn right (-5) degrees
}

// If-else statement use two sets of brackets
if ((2) equals (2)) then {
    turn right (1) degrees
} else {
    turn left (1) degrees
}

// Loops can be stacked infinitely
repeat(2) {
    repeat(2) {
        repeat(2) {
            turn right (4) degrees
        }
    }
}

// So can operators
turn left (add (add (add (add (add (add (1) and (1)) and (1)) and (1)) and (1)) and (1)) and (1)) degrees

// Custom functions can be created with the 'def' keyword.
def do (this) thing { // DO NOT USE PARAMETERS THAT ARE GLOBAL VARIABLES.
    // Indentation is not required but it is good for visibility.
    turn right (this) degrees
}

// The function can then be called like this
do (2) thing

// Dropdown blocks need to have their value explicitly stated
stop ("all")  // Strings still need parenthesis.
```

Write this into `script.st` and run:

```sh
scratchtext script.st
```


You can now open [Scratch](https://scratch.mit.edu/projects/editor/), Go to `File > Load from your computer` and
chose the generated `Project.sb3`.

_For more examples, please refer to the [Documentation](https://pyscratch.readthedocs.io/en/latest/)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->

## Roadmap

- [x] Create a block-generating framework.
- [x] Create a basic scripting language.
- [x] Add a Pip package.
- [ ] Add function and script importing support.
- [ ] Make operators easier to type (eg `a = 10` instead of `set (a) to (10)`).
- [ ] Add the rest of the Scratch blocks.
- [ ] Instant Scratch GUI project loading.
- [ ] Potential [ScratchBlocks](https://github.com/scratchblocks/scratchblocks) integration.

See the [open issues](https://github.com/IfanSnek/PyScratch/issues) for a full list of proposed features (and known
issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

Ethan Porcaro - ethan@ethanporcaro.com

Project Link: [https://github.com/IfanSnek/PyScratch/](https://github.com/IfanSnek/PyScratch/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

* [Scratch Wiki](https://en.scratch-wiki.info/wiki/Scratch_File_Format) for useful information on the .sb3 format.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/IfanSnek/PyScratch.svg?style=for-the-badge

[contributors-url]: https://github.com/IfanSnek/PyScratch/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/IfanSnek/PyScratch.svg?style=for-the-badge

[forks-url]: https://github.com/IfanSnek/PyScratch/network/members

[stars-shield]: https://img.shields.io/github/stars/IfanSnek/PyScratch.svg?style=for-the-badge

[stars-url]: https://github.com/IfanSnek/PyScratch/stargazers

[issues-shield]: https://img.shields.io/github/issues/IfanSnek/PyScratch.svg?style=for-the-badge

[issues-url]: https://github.com/IfanSnek/PyScratch/issues

[license-shield]: https://img.shields.io/github/license/IfanSnek/PyScratch.svg?style=for-the-badge

[license-url]: https://github.com/IfanSnek/PyScratch/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/linkedin_username

[product-screenshot]: images/screenshot.png