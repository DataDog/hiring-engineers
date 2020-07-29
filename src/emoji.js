import React from 'react'
import styled from 'styled-components'

const EmojiImg = styled.img`
  display: inline-block;
`

const EmojiWrapper = styled.span`
  display: inline-grid;
  margin-right: ${({ marginRight }) => marginRight || '10px'};
  width: ${({ size }) => size};
`

export function Emoji({ name, size = '32px', marginRight = '10px' }) {
  return (
    <EmojiWrapper size={size} marginRight={marginRight}>
      <EmojiImg style={{ width: size }} src={require(`../assets/${name}`)} />
    </EmojiWrapper>
  )
}
