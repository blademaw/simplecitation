# simplecitation
A simple script to quickly parse BibTex/RIS strings/files. Made to quickly grab metadata from scientific papers in a useful format.

## Usage

```bash
$ ./getcitation.py FILENAME [bibtex|ris]
```

Supply the filename and, if the file is a `.txt` file, the citation format of the `.txt` file contents. This returns a plaintext citation in the format:

> `author` (`year`). `title`. `journal`, `doi`

Any missing data are substituted with the placeholder "No [datum\_label]," e.g. "No author."

Note that this does not aim to conform to any popular standardized format (APA 7, Chicago, etc.) but instead act as a way to quickly, succinctly describe the contents of a paper (e.g., for reference management.)

### Examples

The paper [Teaching Computational Modeling in the Data Science Era](https://www.sciencedirect.com/science/article/pii/S1877050916310055), for example, can be cited in pure BibTex (`.bib`) form via:

```bash
$ ./getcitation.py bib.bib
```

which outputs

```
Philippe J. Giabbanelli and Vijay K. Mago (2016). Teaching Computational Modeling in the Data Science Era. Procedia Computer Science, https://doi.org/10.1016/j.procs.2016.05.517
```

Alternatively, the same paper could be cited via a `.txt` file containing a RIS citation, via:

```bash
$ ./getcitation.py textris.txt ris
```

which returns the same string as the BibTex example.



## Dependencies
* Uses [BibtexParser](https://bibtexparser.readthedocs.io/en/master/) for parsing BibTex (`.bib`) files
* Uses [rispy](https://pypi.org/project/rispy/#description) for parsing `.ris` files

