import { Appear, Notes } from 'mdx-deck'
import React from 'react'

export function AppearList({ children }) {
  return (
    <>
      <ul>
        <Appear>{children}</Appear>
      </ul>
      <Notes>
        <ul>{children}</ul>
      </Notes>
    </>
  )
}
