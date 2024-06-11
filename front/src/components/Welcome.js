import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { Spring, animated } from 'react-spring';
import HomeIcon from '@mui/icons-material/Home';
import AssignmentIcon from '@mui/icons-material/Assignment';
import ImportantDevicesIcon from '@mui/icons-material/ImportantDevices';
import AnnouncementIcon from '@mui/icons-material/Announcement';

function Welcome() {
  return (
    <Container maxWidth="md" style={{ marginTop: '50px', backgroundColor: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
      <Spring
        from={{ opacity: 0, transform: 'translate3d(0,-40px,0)' }}
        to={{ opacity: 1, transform: 'translate3d(0,0px,0)' }}
      >
        {props => (
          <animated.div style={props}>
            <Typography variant="h3" component="h1" gutterBottom>
              Welcome!
            </Typography>
          </animated.div>
        )}
      </Spring>

      <Spring
        from={{ opacity: 0, transform: 'translate3d(0,-20px,0)' }}
        to={{ opacity: 1, transform: 'translate3d(0,0px,0)' }}
        delay={200}
      >
        {props => (
          <animated.div style={props}>
            <Typography variant="body1" gutterBottom>
              このサイトは機械学習講習会用のオンラインジャッジです。
              <br />
              講習会の演習問題の提出・採点、順位表の確認ができます。
            </Typography>
          </animated.div>
        )}
      </Spring>

      <Spring
        from={{ opacity: 0, transform: 'translate3d(0,-20px,0)' }}
        to={{ opacity: 1, transform: 'translate3d(0,0px,0)' }}
        delay={400}
      >
        {props => (
          <animated.div style={props}>
            <Box display="flex" alignItems="center" style={{ marginBottom: '8px' }}>
              <AssignmentIcon style={{ marginRight: '8px', color: '#ff5722' }} />
              <Typography variant="h4" component="h2">
                Usage
              </Typography>
            </Box>
            <Typography variant="body1" gutterBottom>
              サイドバーから問題を選択してください。
            </Typography>
          </animated.div>
        )}
      </Spring>

      <Spring
        from={{ opacity: 0, transform: 'translate3d(0,-20px,0)' }}
        to={{ opacity: 1, transform: 'translate3d(0,0px,0)' }}
        delay={600}
      >
        {props => (
          <animated.div style={props}>
            <Box display="flex" alignItems="center" style={{ marginBottom: '8px' }}>
              <ImportantDevicesIcon style={{ marginRight: '8px', color: '#ff5722' }} />
              <Typography variant="h4" component="h2">
                Environment
              </Typography>
            </Box>
            <Typography variant="body1" gutterBottom>
              ジャッジは以下の環境で実行されます。
            </Typography>

            <Typography variant="body1" component="pre" gutterBottom>
              Python 3.11
              <br />
              numpy==1.26.4
              <br />
              torch==2.3.0
              <br />
              scikit-learn==1.5.0
            </Typography>
          </animated.div>
        )}
      </Spring>

      <Spring
        from={{ opacity: 0, transform: 'translate3d(0,-20px,0)' }}
        to={{ opacity: 1, transform: 'translate3d(0,0px,0)' }}
        delay={800}
      >
        {props => (
          <animated.div style={props}>
            <Box display="flex" alignItems="center" style={{ marginBottom: '8px' }}>
              <AnnouncementIcon style={{ marginRight: '8px', color: '#ff5722' }} />
              <Typography variant="h4" component="h2">
                Note
              </Typography>
            </Box>
            <Typography variant="body1" gutterBottom>
              システムへの攻撃は禁止です。問題を解く際には他の参加者に迷惑をかけないようにしてください。
              <br />

              (迷惑をかけずに脆弱性を見つけたい人は大歓迎なので @abap34 まで連絡してください。 Repository に招待します。)
            </Typography>
          </animated.div>
        )}
      </Spring>
    </Container>
  );
}

export default Welcome;
