import { Container, Row, Spacer } from "@nextui-org/react";
import { Loading } from "@nextui-org/react";

export default function Home() {
	return (
		<Container>
			<Row justify="center" align="center" fluid>
				<Spacer y={20}/>
					<Loading />
			</Row>
		</Container>
	);
}
