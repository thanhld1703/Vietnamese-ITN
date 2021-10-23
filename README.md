# Vietnamese-ITN
Convert vietnamese words in spoken form to written form, e.g `một phẩy hai mét -> 1,2 m`

Install dependency: 
```
conda install -c conda-forge -y pynini=2.1.4
```

Usage: 
``` python
python inverse_normalize_beta.py "một hai ba"
python inverse_normalize_beta.py "năm hai nghìn linh năm tỷ lệ lạm phát đạt mức mười hai phẩy năm phần trăm ba năm hai nghìn mười sáu hai nghìn mười ba và hai nghìn mười bốn tỷ lệ lạm phát không đổi là mười hai phẩy mười hai phần trăm"
```

## For developer
### Export
- Refer to this [script](./export.sh).
### Tutorials
- Refer to this [link](http://wellformedness.com/courses/pynini/) or this [notebook](./algorithms.ipynb) for briefs.
