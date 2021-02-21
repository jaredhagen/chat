import axios from "axios";
import { DateTime } from "luxon";
import { useMutation, useQueryClient } from "react-query";

import { useAuth } from "./useAuth";

// See: https://react-query.tanstack.com/guides/optimistic-updates
export default function usePostMessage(roomId) {
  const queryClient = useQueryClient();
  const auth = useAuth();
  const messagesQueryKey = ["messages", roomId];
  return useMutation(
    async (newMessage) => {
      const response = await axios.post(
        `${process.env.REACT_APP_CHAT_API_ENDPOINT}/rooms/${roomId}/messages`,
        newMessage,
        {
          headers: {
            Authorization: `Bearer ${auth.username}`,
          },
        }
      );
      return response.data;
    },
    {
      onMutate: async (newMessage) => {
        await queryClient.cancelQueries(messagesQueryKey);
        const previousMessages = queryClient.getQueryData(messagesQueryKey);
        queryClient.setQueryData(messagesQueryKey, (old) => ({
          messages: [
            // New messages should go at the front of the array
            // because messages are displayed in reverse order
            {
              id: "temp",
              author: auth.username,
              content: newMessage.content,
              createdAt: DateTime.now().toMillis(),
            },
            ...old.messages,
          ],
        }));

        return { previousMessages };
      },
      onError: (err, newMessage, context) => {
        queryClient.setQueryData(messagesQueryKey, context.previousMessages);
      },
      onSettled: () => {
        queryClient.invalidateQueries(messagesQueryKey);
        queryClient.invalidateQueries("rooms");
      },
    }
  );
}
