import React from 'react'
import styled from 'styled-components'

import { Emoji } from './emoji'
import { AppearList } from './appear-list'

const CenteredLi = styled.li`
  display: flex;
  align-items: center;
  padding: 10px;
`

export function AboutMe() {
  return (
    <>
      <h2 style={{ margin: 0 }}>I'm Matt</h2>

      <AppearList style={{ margin: 0 }}>
        <CenteredLi>
          <Emoji size="40px" marginRight="30px" name="wave-circle.png" />
          Wealthfront
        </CenteredLi>

        <CenteredLi>
          <Emoji size="40px" marginRight="30px" name="drift.png" />
          Drift
        </CenteredLi>

        <CenteredLi>
          <Emoji size="40px" marginRight="30px" name="ld.png" />
          LaunchDarkly
        </CenteredLi>
      </AppearList>
    </>
  )
}
