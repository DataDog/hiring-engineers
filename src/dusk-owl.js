export const duskOwl = {
  colors: {
    background: '#222',
    text: '#d6deeb',
    primary: 'rgb(173, 219, 103)',
  },
  styles: {
    CodeSurfer: {
      pre: {
        color: 'text',
        backgroundColor: 'background',
      },
      code: {
        color: 'text',
        backgroundColor: 'background',
      },
      tokens: {
        boolean: { color: 'rgb(255, 88, 116)' },
        'builtin char constant function': {
          color: 'rgb(130, 170, 255)',
        },
        changed: {
          color: 'rgb(162, 191, 252)',
          fontStyle: 'italic',
        },
        'class-name': { color: 'rgb(255, 203, 139)' },
        comment: {
          color: 'rgb(99, 119, 119)',
          fontStyle: 'italic',
        },
        deleted: {
          color: 'rgba(239, 83, 80, 0.56)',
          fontStyle: 'italic',
        },
        'inserted attr-name': {
          color: 'rgb(173, 219, 103)',
          fontStyle: 'italic',
        },
        namespace: { color: 'rgb(178, 204, 214)' },
        number: { color: 'rgb(247, 140, 108)' },
        property: { color: 'rgb(128, 203, 196)' },
        punctuation: { color: 'rgb(199, 146, 234)' },
        'selector doctype': {
          color: 'rgb(199, 146, 234)',
          fontStyle: 'italic',
        },
        'string url': { color: 'rgb(173, 219, 103)' },
        'tag operator keyword': {
          color: 'rgb(127, 219, 202)',
        },
        variable: { color: 'rgb(214, 222, 235)' },
      },
      title: {
        backgroundColor: '#222',
        color: 'text',
      },
      subtitle: {
        color: '#d6deeb',
        backgroundColor: 'rgba(10,10,10,0.9)',
      },
      unfocused: {
        // only the opacity of unfocused code can be changed
        opacity: 0.1,
      },
    },
  },
}
