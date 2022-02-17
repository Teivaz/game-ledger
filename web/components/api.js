import { useEffect, useState } from "react";

/*** Returns current user object if the user is logged in.
 * Initial value is `undefined`.
 * The user will be set to the object when request is completed successfully.
 * If the user is not logged in the value would be `null`.
 */
export function useCurrentUser() {
  const [user, setUser] = useState(undefined);
  useEffect(() => {
    fetch("/api/user/")
      .then((response) => {
        if (response.ok) {
          response
            .json()
            .then(j=>setUser(j[0]))
            .catch(() => setUser(null));
        } else {
          setUser(null);
        }
      })
      .catch(() => setUser(null));
  }, []);
  return user;
}
