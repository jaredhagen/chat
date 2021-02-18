import axios from "axios";
import { useMutation } from "react-query";
import { useAuth } from "./useAuth";

// See: https://react-query.tanstack.com/guides/optimistic-updates
export default function useUserLogin() {
  const auth = useAuth();

  return useMutation(
    async (credentials) => {
      const response = await axios.post(
        `http://localhost:5000/users`,
        credentials
      );
      return response.data;
    },
    {
      onSettled: (data) => {
        const user = {
          username: data.username,
          token: data.username,
        };
        auth.logIn(user);
      },
      onError: () => {
        console.log("hmmmmmmmm");
      },
    }
  );
}
