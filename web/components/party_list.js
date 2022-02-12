import {
	Row, Loading,
	Avatar, Grid, Card,
	Text
} from "@nextui-org/react";
import { useState } from "react";
import { useRouter } from "next/router";

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
export default function PartyList() {
	const [loading, setLoading] = useState(false);
	const router = useRouter();

	const parties = _parties_mock;

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
					<Card
						hoverable
						clickable
						width="100%"
						onClick={() => router.push(`/party/${party.id}/`)}
					>
						<Card.Body
							css={{ p: 0, flexDirection: "row", alignItems: "center" }}
						>
							<Avatar bordered color="primary" src="/avatar-1.png" size="lg" />
							<Text>{party.name}</Text>
						</Card.Body>
					</Card>
				</Grid>
			))}
		</Grid.Container>
	);
}
