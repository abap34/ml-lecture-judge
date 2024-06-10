import React from 'react';
import { Container, Typography } from '@mui/material';

function Welcome() {
  return (
    <Container maxWidth="md" style={{ marginTop: '50px', backgroundColor: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome!
      </Typography>

      <Typography variant="body1" gutterBottom>
        このサイトは機械学習講習会用のオンラインジャッジです。
        <br />
        講習会の演習問題の提出・採点、順位表の確認ができます。
      </Typography>

      <Typography variant="h4" component="h2" gutterBottom>
        &gt; Usage
      </Typography>
      <Typography variant="body1" gutterBottom>
        サイドバーから問題を選択してください。
      </Typography>

      <Typography variant="h4" component="h2" gutterBottom>
        &gt; Environment
      </Typography>

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

      <Typography variant="h4" component="h2" gutterBottom>
        &gt; Note
      </Typography>

      <Typography variant="body1" gutterBottom>
        時間の計測はやや適当に実装されています。 正確にベンチマークしたい場合は手元で実行してください。 
        <br />

        システムへの攻撃は禁止です。問題を解く際には他の参加者に迷惑をかけないようにしてください。

        <br />

        (迷惑をかけずに脆弱性を見つけたい人は大歓迎なので @abap34 まで連絡してください。 Repository に招待します。)
      </Typography>

    </Container>
  );
}

export default Welcome;
