# simplecitation
A simple script to quickly parse BibTex/RIS strings/files. Made to quickly grab metadata from scientific papers in a useful text format.

## Usage

```bash
$ ./getcitation.py [FILENAME [bibtex|ris]]
```

Supply the filename to retrieve a plaintext citation for a `.bib` or `.ris` file. If a `.txt` file is supplied, the citation format of the contents will be automatically detected, or may be explicitly supplied as an additional argument.

Alternatively, supplying no filename parses contents in the clipboard, automatically detecting the citation format.

Outputted plaintext citations are in the format:

> `author(s)` (`year`). `(primary) title`. `journal`, `doi`

Any missing data are substituted with the placeholder "No [datum\_label]," e.g. "No author."

Note that this does not aim to conform to any popular standardized format (APA 7, Chicago, etc.) but instead acts as a way to quickly, succinctly describe the contents of a paper (e.g., for personal reference management.)

### Examples

The paper [Teaching Computational Modeling in the Data Science Era](https://www.sciencedirect.com/science/article/pii/S1877050916310055), for example, can be cited in pure BibTex (`.bib`) form via:

```bash
$ ./getcitation.py bib.bib
```

which outputs

```
Philippe J. Giabbanelli and Vijay K. Mago (2016). Teaching Computational Modeling in the Data Science Era. Procedia Computer Science, https://doi.org/10.1016/j.procs.2016.05.517
```



A citation formatted as a `.txt` file containing an RIS citation would be parsed via:

```bash
$ ./getcitation.py biofilms.txt [ris]
```

where the `[ris]` format argument is optional. When parsed for the paper [Strategies for combating bacterial biofilm infections](https://www.nature.com/articles/ijos201465), the output is the following:

```
Hong Wu, Claus Moser, Heng-Zhuang Wang, Niels Høiby, Zhi-Jun Song (2015). Strategies for combating bacterial biofilm infections. International Journal of Oral Science, 10.1038/ijos.2014.65
```



## Dependencies
* Uses [BibtexParser](https://bibtexparser.readthedocs.io/en/master/) for parsing BibTex (`.bib`) files
* Uses [rispy](https://pypi.org/project/rispy/#description) for parsing `.ris` files
* Uses [pyperclip](https://pypi.org/project/pyperclip/) for clipboard access

