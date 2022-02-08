import {
  Container,
  Row,Col,
  Spacer,
  Loading,
  Avatar,
  Input,
  Grid,
  Button,Card,Text, User,
} from "@nextui-org/react";
import { useState } from "react";
import { useRouter } from 'next/router'

const _user_mock = {
	id: 1,
	email: "email@user.com",
	name: "Strategic Thinker 666",
	profile_image: "/avatar-1.png",
	parties: [1, 2],
	owned_games: [1, 2, 3],
}

export default function UserPage() {
	const user = _user_mock
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

function UserView({user}) {
  const tabs = [
    { name: "Parties", component: Parties },
    { name: "Games", component: Games },
  ];

  const [activeTab, setActiveTab] = useState(tabs[0].name);

  const TabComponent = tabs.filter((e) => e.name === activeTab)[0].component;
  return (
    <div style={{ height: "100%" }}>
      <Row>
        <Container justify="center">
          <Row justify="center" fluid>
            <Avatar bordered color="primary" src={user.profile_image} size="xl" />
          </Row>
          <Row justify="center" fluid>
            {/* <Input justify="center" placeholder="Next UI" /> */}
						<Text h3>{user.name}</Text>
          </Row>
        </Container>
      </Row>
      <Row>
        <Grid.Container gap={2} justify="center">
          {tabs.map((e) => (
            <Grid fluid key={e.name}>
              <Button
                size="xs"
                bordered={e.name !== activeTab}
                onClick={() => setActiveTab(e.name)}
              >
                {e.name}
              </Button>
            </Grid>
          ))}
        </Grid.Container>
      </Row>
      <Row fluid>
        <TabComponent />
      </Row>
    </div>
  );
}

const _parties_mock = [
  {
    id: 1,
		name: "Party Poopers",
		profile_image: "/avatar-1.png",
		members: [1, 2],
		games: [1, 2, 3],
		game_sessions: [1, 2, 3],
  },
  {
    id: 2,
    name: "The Eclippers",
    profile_image: "/avatar-1.png",
		members: [1, 2],
		games: [1, 2, 3],
		game_sessions: [1, 2, 3],
  },
];


function Parties() {
  const [loading, setLoading] = useState(false);
	const router = useRouter();

	const parties = _parties_mock

  if (loading)
    return (
      <Row justify="center" fluid>
        <Loading />
      </Row>
    );
  return (
		<Grid.Container gap={2} justify="flex-start">
      {parties.map((party) => (
				<Grid fluid={1} key={party.id}>
				<Card hoverable clickable width="100%" onClick={()=>router.push(`/party/${party.id}/`)}>
					<Card.Body css={{ p: 0, flexDirection: 'row', alignItems: "center" }}>
            <Avatar bordered color="primary" src="/avatar-1.png" size="lg" />
						<Text>{party.name}</Text>
					</Card.Body>
				</Card>
			</Grid>
				))}
		</Grid.Container>
  );
}

const _games_mock = [
  {
    id: 1,
    name: "Munchkin",
    revision: "",
    rules: "some rules go here",
    profile_image: "/avatar-1.png",
    images: [],
    custom_fields: {},
    author: 0,
    access_level: "public",
  },
  {
    id: 2,
    name: "Eclipse",
    revision: "",
    rules: "some eclipse rules go here",
    profile_image: "/avatar-1.png",
    images: [],
    custom_fields: {},
    author: 0,
    access_level: "public",
  },
  {
    id: 2,
    name: "Eclipse",
    revision: "",
    rules: "some eclipse rules go here",
    profile_image: "/avatar-1.png",
    images: [],
    custom_fields: {},
    author: 0,
    access_level: "public",
  },
];

function Games() {
  const [loading, setLoading] = useState(false);
	const router = useRouter();

  const games = _games_mock;

  if (loading)
    return (
      <Row justify="center" fluid>
        <Loading />
      </Row>
    );

  return (
		<Grid.Container gap={2} justify="flex-start">
      {games.map((game) => (
				<Grid xs={6} sm={3} key={game.id}>
				<Card hoverable clickable width="100%" onClick={()=>router.push(`/game/${game.id}/`)}>
					<Card.Body css={{ p: 0 }}>
						<Card.Image
							objectFit="cover"
							src={game.profile_image}
							width='100%'
							height={80}
							alt={game.name}
						/>
					</Card.Body>
					<Card.Footer justify="flex-start">
						<Row justify="space-between">
							<Text b>
								{game.name}
							</Text>
						</Row>        
					</Card.Footer>
				</Card>
			</Grid>
				))}
		</Grid.Container>
  );
}
