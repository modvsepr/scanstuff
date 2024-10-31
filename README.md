# Project Title

Scanstuff - A minimal code for fixing scanned notes

## Description

I took a lot of handwritten notes in the past and need to have a digital copy of them.
Everytime I scan an old notebook I face issues of having a final PDF with homogeneous-looking pages.
There are several solutions over the Internet and some of them are amazing, however I needed something simple to avoid the steep learning curve that most of the other solutions have.

This Python code read the original scanned PDF, crops your scanned pages (you can scan a full double page or one single page separately) and you have the option to use OpenCV for improving contrast and lightening background.

## Getting Started

### Dependencies

* Python 3.x
* Install the following packages:
```
$ pip install numpy opencv-python pillow pdf2image
```

### Usage example

* Put the original PDF in the same folder where the Python code is located and type:
```
$ python3 scanstuff.py -f filename -t 20 -b 20 -m 30 -w 2400 -d -i
```
* _-f filename_ - name of the original PDF name without extension.
* _-t 20_ - pixels to be removed from the top margin.
* _-b 20_ - pixels to be removed from the bottom margin.
* _-m 30_ - pixels to be removed from the inner margin on the binding side (if -d option is used), or pixels to be removed from the right margin.
* _-w 2400_ - pixel of the page width. If 0 is set, the width of the original page is used. 
* _-d_ - splits double pages in the original scanned PDF
* _-i_ - improves contrast and readability

## Help

```
$ python3 scanstuff.py --help
```

## Authors

vsepr

## Version History

* 20241030
    * Initial Release

## License

This project is licensed under the GPL-3.0 License.

## Acknowledgments

Some inspirational and amazing software:
* [unpaper](https://github.com/unpaper/unpaper)
