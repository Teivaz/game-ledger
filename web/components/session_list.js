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

const _sessions_mock = [
  {
    id: 1,
    game: 1,
    session_date: "2022-02-12T21:52:37+00:00",
    session_duration: "35m",
    party: 1,
    participants: [1, 2, 3],
    scores: { [1]: 1, [2]: 1, [3]: 2 },
    custom_fields: {},
  },
  {
    id: 2,
    game: 1,
    session_date: "2022-02-10T21:52:37+00:00",
    session_duration: "25m",
    party: 1,
    participants: [1, 2, 3],
    scores: { [1]: 1, [2]: 3, [3]: 2 },
    custom_fields: {},
  },
];

export default function SessionList() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const sessions = _sessions_mock;

  if (loading)
    return (
      <Row justify="center" fluid>
        <Loading />
      </Row>
    );

  return (
    <Grid.Container gap={2} justify="flex-start">
      {sessions.map((session) => (
        <Grid xs={6} sm={3} key={session.id}>
          <Card
            hoverable
            clickable
            width="100%"
            onClick={() => router.push(`/session/${session.id}/`)}
          >
            <Card.Body css={{ p: 0 }}>
              <Card.Image
                objectFit="cover"
                src={session.profile_image}
                width="100%"
                height={80}
                alt="session"
              />
            </Card.Body>
            <Card.Footer justify="flex-start">
              <Row justify="space-between">
                <Text b>Sunday 13th</Text>
              </Row>
            </Card.Footer>
          </Card>
        </Grid>
      ))}
    </Grid.Container>
  );
}
