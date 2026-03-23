#let data = json("resume.json")

#let accent = rgb("#13233A")
#let accent-soft = rgb("#4C5A6B")
#let rule = rgb("#D6DBE1")

#set page(
  paper: "a4",
  margin: (
    top: 1.25cm,
    bottom: 1.2cm,
    left: 1.45cm,
    right: 1.45cm,
  ),
)

#set text(
  font: "Libertinus Serif",
  size: 10.2pt,
  fill: accent,
  lang: "en",
)

#set par(justify: false, leading: 0.66em)

#let field(value) = {
  if value == none { [] } else if type(value) == array and value.len() == 0 { [] } else if value == "" { [] } else { value }
}

#let join-nonempty(items, sep: "  |  ") = {
  let filtered = items.filter(item => {
    item != none and item != ""
  })
  filtered.join(sep)
}

#let section(title, body) = {
  if body == none or body == [] { [] } else [
    #v(0.9em)
    #block[
      #text(weight: 700, size: 8.8pt, tracking: 0.18em, fill: accent-soft)[#title]
      #v(0.3em)
      #line(length: 100%, stroke: (paint: rule, thickness: 0.65pt))
      #v(0.35em)
      #body
    ]
  ]
}

#let bullet-list(items) = {
  if items == none or items.len() == 0 { [] } else [
    #set list(marker: [•], indent: 1.1em, body-indent: 0.45em, spacing: 0.24em)
    #list(..items)
  ]
}

#let experience-entry(item) = [
  #grid(
    columns: (1fr, auto),
    column-gutter: 1.2em,
    [
      #text(weight: 700)[#item.at("title", default: "Role")]
      #if field(item.at("company", default: none)) != [] {
        [ at #item.at("company")]
      }
      #if field(item.at("location", default: none)) != [] {
        [ • #item.at("location")]
      }
    ],
    [
      #text(fill: accent-soft)[#join-nonempty((item.at("start", default: none), item.at("end", default: none)), sep: " - ")]
    ],
  )
  #if field(item.at("subtitle", default: none)) != [] [
    #text(style: "italic", fill: accent-soft)[#item.at("subtitle")]
    #v(0.15em)
  ]
  #bullet-list(item.at("bullets", default: ()))
  #v(0.45em)
]

#let project-entry(item) = [
  #text(weight: 700)[#item.at("name", default: "Project")]
  #if field(item.at("subtitle", default: none)) != [] [
    #text(fill: accent-soft)[  •  #item.at("subtitle")]
  ]
  #v(0.1em)
  #bullet-list(item.at("bullets", default: ()))
  #v(0.45em)
]

#let education-entry(item) = [
  #grid(
    columns: (1fr, auto),
    column-gutter: 1.2em,
    [
      #text(weight: 700)[#item.at("school", default: "Institution")]
      #if field(item.at("degree", default: none)) != [] {
        [ — #item.at("degree")]
      }
      #if field(item.at("location", default: none)) != [] {
        [ • #item.at("location")]
      }
    ],
    [
      #text(fill: accent-soft)[#join-nonempty((item.at("start", default: none), item.at("end", default: none)), sep: " - ")]
    ],
  )
  #v(0.35em)
]

#align(center)[
  #text(size: 19pt, weight: 800, tracking: 0.03em)[#data.at("name", default: "Candidate Name")]
  #v(0.18em)
  #if field(data.at("title", default: none)) != [] [
    #text(size: 10pt, fill: accent-soft, weight: 500)[#data.at("title")]
    #v(0.25em)
  ]
  #text(size: 9pt, fill: accent-soft)[
    #join-nonempty((
      data.at("location", default: none),
      data.at("phone", default: none),
      data.at("email", default: none),
      data.at("website", default: none),
      data.at("linkedin", default: none),
    ))
  ]
]

#section("Professional Summary", [
  #bullet-list(data.at("summary", default: ()))
])

#section("Core Skills", [
  #text(fill: accent)[#data.at("skills", default: ()).join("  •  ")]
])

#section("Experience", [
  #for item in data.at("experience", default: ()) [
    #experience-entry(item)
  ]
])

#section("Selected Projects", [
  #for item in data.at("projects", default: ()) [
    #project-entry(item)
  ]
])

#section("Education", [
  #for item in data.at("education", default: ()) [
    #education-entry(item)
  ]
])

#section("Additional Information", [
  #if field(data.at("certifications", default: ())) != [] [
    #text(weight: 700)[Certifications:]
    #text(fill: accent-soft)[ #data.at("certifications").join(", ")]
    #linebreak()
  ]
  #if field(data.at("languages", default: ())) != [] [
    #text(weight: 700)[Languages:]
    #text(fill: accent-soft)[ #data.at("languages").join(", ")]
    #linebreak()
  ]
])
