import {
  Container,
  Row,
  Col,
  Spacer,
  Loading,
  Avatar,
  Input,
  Grid,
  Button,
  Text,
  User,
} from "@nextui-org/react";
import { useState } from "react";
import GameList from "../../components/game_list"
import PartyList from "../../components/party_list";
import SessionList from "../../components/session_list";

const _user_mock = {
  id: 1,
  email: "email@user.com",
  name: "Strategic Thinker 666",
  profile_image: "/avatar-1.png",
  parties: [1, 2],
  owned_games: [1, 2, 3],
};

export default function UserPage() {
  const user = _user_mock;
  return (
    <div>
      <UserView user={user} />
    </div>
  );
}

function LoadingView() {
  return (
    <Row justify="center" align="center" fluid>
      <Spacer y={20} />
      <Loading />
    </Row>
  );
}

function UserView({ user }) {
  const tabs = [
    { name: "Parties", component: PartyList },
    { name: "Sessions", component: SessionList },
    { name: "Games", component: GameList },
  ];

  const [activeTab, setActiveTab] = useState(tabs[0].name);

  const TabComponent = tabs.filter((e) => e.name === activeTab)[0].component;
  return (
    <div style={{ height: "100%" }}>
      <Row>
        <Container justify="center">
          <Row justify="center" fluid>
            <Avatar
              bordered
              color="primary"
              src={user.profile_image}
              size="xl"
            />
          </Row>
          <Row justify="center" fluid>
            {/* <Input justify="center" placeholder="Next UI" /> */}
            <Text h3>{user.name}</Text>
          </Row>
        </Container>
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
        <TabComponent />
      </Row>
    </div>
  );
}


