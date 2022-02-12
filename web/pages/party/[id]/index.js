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
import { useState } from "react"
import GameList from "../../../components/game_list";
import SessionList from "../../../components/session_list";

const _party_mock = {
  id: 1,
  name: "Party Poopers",
  profile_image: "/avatar-1.png",
  members: [1, 2],
  games: [1, 2, 3],
  game_sessions: [1, 2, 3],
};

export default function GameView() {
  const tabs = [
    { name: "Sessions", component: SessionList },
    { name: "Games", component: GameList },
    { name: "Members", component: Members },
  ];

  const [activeTab, setActiveTab] = useState(tabs[0].name);

  const TabComponent = tabs.filter((e) => e.name === activeTab)[0].component;

  const party = _party_mock;
  return (
    <Container>
      <Row>
        <Col>
          <Avatar squared color="primary" src={party.profile_image} size="xl" />
        </Col>
        <Col>
          <Text h3>Party</Text>
          <Text h4>{party.name}</Text>
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
        <TabComponent party={party} />
      </Row>
    </Container>
  );
}

function Members() {
  return <div></div>;
}


