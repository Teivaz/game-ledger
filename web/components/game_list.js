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
  Card,
  Text,
  User,
} from "@nextui-org/react";
import { useState } from "react";
import { useRouter } from "next/router";

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

export default function GameList() {
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
          <Card
            hoverable
            clickable
            width="100%"
            onClick={() => router.push(`/game/${game.id}/`)}
          >
            <Card.Body css={{ p: 0 }}>
              <Card.Image
                objectFit="cover"
                src={game.profile_image}
                width="100%"
                height={80}
                alt={game.name}
              />
            </Card.Body>
            <Card.Footer justify="flex-start">
              <Row justify="space-between">
                <Text b>{game.name}</Text>
              </Row>
            </Card.Footer>
          </Card>
        </Grid>
      ))}
    </Grid.Container>
  );
}
