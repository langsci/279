(TeX-add-style-hook
 "01-introduction"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("langscibook" "output=paper" "modfonts")))
   (TeX-run-style-hooks
    "latex2e"
    "../localpackages"
    "localcommands"
    "langscibook"
    "langscibook10")
   (LaTeX-add-labels
    "fig-structure1"
    "sec-connections"
    "tab-ms-model"
    "tab-muysken_OS"
    "tab-muysken_CS"
    "tab-muysken"
    "framework"
    "fig-structure2")
   (LaTeX-add-bibliographies
    "localbibliography"
    "../localbibliography"))
 :latex)

