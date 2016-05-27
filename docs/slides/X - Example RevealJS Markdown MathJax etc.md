---
layout: slides
lang: en
theme: moon
transition: fade  # none/fade/slide/convex/concave/zoom
center: false
revealjs-url: http://lab.hakim.se/reveal-js
# fails because CDNs don't serve up /css etc
# revealjs-url: https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.3.0/js/reveal.min.js
# build with `./build`
# serve the HTML at http://localhost:8000/ with `python -m SimpleHTTPServer`
---

# [MathJax Matrix Example](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

$$A_{m,n} = 
 \begin{pmatrix}
  a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
  a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
 \end{pmatrix}$$


# [MathJax Sum and Speaker Note](https://github.com/hakimel/reveal.js/blob/dev/README.md#slide-transitions)

$$\sum_{\substack{
   0<i<m \\
   0<j<n
  }} 
 P(i,j)$$

<aside class="notes">
    Oh hey, these are some notes. They'll be hidden in your presentation, but you can see them if you open the speaker notes window (hit 's' on your keyboard).
</aside>



