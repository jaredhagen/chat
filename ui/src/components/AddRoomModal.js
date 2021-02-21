import { createContext, useState } from "react";
import { Button, Form, Input, Modal } from "antd";

import { usePostRoom } from "../hooks";

const AddRoomModalContext = createContext();

function AddRoomModalProvider({ children }) {
  const [isVisibile, setIsVisible] = useState(false);
  const postRoom = usePostRoom();
  const [form] = Form.useForm();

  const showModal = () => {
    setIsVisible(true);
  };

  const hideModal = () => {
    setIsVisible(false);
  };

  const onFinish = (newRoom) => {
    postRoom.mutate(newRoom, {
      onSuccess: () => {
        hideModal();
        form.resetFields();
      },
    });
  };

  return (
    <AddRoomModalContext.Provider value={{ showModal }}>
      {children}
      <Modal
        title="Add a Room"
        destroyOnClose
        footer={null}
        onCancel={hideModal}
        visible={isVisibile}
      >
        <Form form={form} name="addRoom" onFinish={onFinish}>
          <Form.Item
            name="id"
            hasFeedback={postRoom.isLoading || postRoom.isError}
            validateStatus={
              postRoom.isLoading
                ? "validating"
                : postRoom.isError
                ? "error"
                : ""
            }
            help={
              postRoom.isError ? "A room with that name already exists" : null
            }
            rules={[
              {
                required: true,
                message: "Please input a room name",
              },
            ]}
          >
            <Input placeholder="Room name" />
          </Form.Item>
          <Form.Item>
            <Button block type="primary" htmlType="submit">
              Add Room
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </AddRoomModalContext.Provider>
  );
}

export { AddRoomModalProvider, AddRoomModalContext };
