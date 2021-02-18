import { useMutation, useQueryClient } from "react-query";
import axios from "axios";

// See: https://react-query.tanstack.com/guides/optimistic-updates
export default function usePostMessage(roomId) {
  const queryClient = useQueryClient();
  const messagesQueryKey = ["messages", roomId];
  return useMutation(
    async (newMessage) => {
      const response = await axios.post(
        `http://localhost:5000/rooms/${roomId}/messages`,
        newMessage,
        {
          headers: {
            Authorization: "Bearer default",
          },
        }
      );
      return response.data;
    },
    {
      onMutate: async (newMessage) => {
        await queryClient.cancelQueries(messagesQueryKey);
        const previousMessages = queryClient.getQueryData(messagesQueryKey);
        queryClient.setQueryData(messagesQueryKey, (old) => {
          console.log(old);
          return {
            messages: [
              ...old.messages,
              {
                id: "temp",
                author: "default",
                ...newMessage,
              },
            ],
          };
        });

        return { previousMessages };
      },
      onError: (err, newMessage, context) => {
        queryClient.setQueryData(messagesQueryKey, context.previousMessages);
      },
      onSettled: () => {
        queryClient.invalidateQueries(messagesQueryKey);
      },
    }
  );
}
