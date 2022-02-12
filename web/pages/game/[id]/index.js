import {
  Container,
  Row,
  Col,
  Avatar,
  Textarea,
  Grid,
  Button,
  Card,
  Text,
} from "@nextui-org/react";
import { useRouter } from "next/router";
import {useState} from 'react'

const _game_mock = {
  id: 1,
  name: "Munchkin",
  revision: "",
  rules: "some rules go here",
  profile_image: "/avatar-1.png",
  images: ["/avatar-1.png"],
  custom_fields: {},
  author: 0,
  access_level: "public",
};

export default function GameView() {
  const tabs = [
    { name: "Rules", component: Rules },
    { name: "Photos", component: Photos },
    { name: "Fields", component: Fields },
  ];

  const [activeTab, setActiveTab] = useState(tabs[0].name);

  const TabComponent = tabs.filter((e) => e.name === activeTab)[0].component;

  const game = _game_mock;
  return (
    <Container>
      <Row>
        <Col>
          <Avatar squared color="primary" src={game.profile_image} size="xl" />
        </Col>
        <Col>
          <Text h3>Game</Text>
          <Text h4>{game.name}</Text>
        </Col>
      </Row>

      <Row>
        <Grid.Container gap={2} justify="center">
          <Button.Group size="xs">
            {tabs.map((e) => (
              <Button
                key={e.name}
                bordered={e.name !== activeTab}
                onClick={() => setActiveTab(e.name)}
              >
                {e.name}
              </Button>
            ))}
          </Button.Group>
        </Grid.Container>
      </Row>
      <Row fluid>
        <TabComponent game={game} />
      </Row>
    </Container>
  );
}

function Rules({game}) {
  return (
  <Textarea
      readOnly
      width="100%"
      initialValue={game.rules}
  />)
}
function Photos({game}) {
  const router = useRouter();

  return (
  <Grid.Container gap={2} justify="flex-start">
    {game.images.map((image) => (
      <Grid xs={6} sm={3} key={image}>
        <Card
          hoverable
          clickable
          width="100%"
          onClick={() => router.push(`/data/${image}/`)}
        >
          <Card.Body css={{ p: 0 }}>
            <Card.Image
              objectFit="cover"
              // src={`/data/api/image/?id=${image}`}
              src={image}
              width="100%"
              height={80}
              alt="image"
            />
          </Card.Body>
        </Card>
      </Grid>
    ))}
  </Grid.Container>
  )
}
function Fields() {
  return <div></div>;
}
