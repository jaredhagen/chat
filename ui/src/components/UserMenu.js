import { Avatar, Button, Popover, Typography } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { useState } from "react";

import { useAuth } from "../hooks";

export default function UserMenu() {
  const auth = useAuth();
  const [popoverVisible, setPopoverVisible] = useState(false);

  return (
    <Popover
      content={
        <Button block onClick={auth.logOut}>
          Logout
        </Button>
      }
      placement="bottom"
      trigger={["click"]}
      arrowPointAtCenter
      visible={popoverVisible}
      onVisibleChange={(visible) => {
        setPopoverVisible(visible);
      }}
    >
      <div style={{ display: "inline-block", cursor: "pointer" }}>
        <Avatar
          style={{ marginTop: "-3px", cursor: "pointer" }}
          shape="square"
          size={32}
          icon={<UserOutlined />}
        />
        <Typography.Text strong style={{ padding: "0 8px", cursor: "pointer" }}>
          {auth.username}
        </Typography.Text>
      </div>
    </Popover>
  );
}
