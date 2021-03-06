import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import { Input, Button, Row, Grid, Loading, User } from "@nextui-org/react";
import { useCurrentUser } from "../components/api";
import { useState } from "react";

function NotLoggedIn() {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");

  function signIn() {
    setLoading(true);
    fetch("/api/user/signin/", {
      method: "POST",
      body: JSON.stringify({ email }),
    })
      .then(() => {})
      .finally(() => setLoading(false));
  }
  function register() {
    setLoading(true);
    fetch("/api/user/register/", {
      method: "POST",
      body: JSON.stringify({ email, name: "I" }),
      headers: { "Content-Type": "application/json" },
    })
      .then(() => {})
      .finally(() => setLoading(false));
  }

  return (
    <Grid>
      <Input
        bordered
        type="email"
        labelPlaceholder="Email"
        onChange={(e) => setEmail(e.target.value)}
        value={email}
      />
      <Row justify="center" align="center" fluid>
        <Button disabled={loading} bordered auto onClick={signIn}>
          Sign In
        </Button>
        <Button disabled={loading} auto onClick={register}>
          Sign Up
        </Button>
      </Row>
    </Grid>
  );
}

export default function Home() {
  const currentUser = useCurrentUser();

  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        {currentUser === undefined ? (
          <Loading />
        ) : currentUser === null ? (
          <NotLoggedIn />
        ) : (
          <div>User: {currentUser.name}</div>
        )}
      </main>
    </div>
  );
}
