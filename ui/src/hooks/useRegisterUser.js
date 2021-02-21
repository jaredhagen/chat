import axios from "axios";
import { useMutation } from "react-query";
import { useAuth } from "./useAuth";

// See: https://react-query.tanstack.com/guides/optimistic-updates
export default function useUserLogin() {
  const auth = useAuth();

  return useMutation(
    async (credentials) => {
      const response = await axios.post(
        `${process.env.REACT_APP_CHAT_API_ENDPOINT}/users`,
        credentials
      );
      return response.data;
    },
    {
      onSettled: (data, error) => {
        if (!error) {
          auth.logIn(data.username);
        }
      },
    }
  );
}
