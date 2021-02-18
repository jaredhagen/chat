import { Avatar, Button, Dropdown, Popover, Row, Typography } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { useState } from "react";

import { useAuth } from "../../auth";

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
      arrowPointAtCenter={true}
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
          Demo User
        </Typography.Text>
      </div>
    </Popover>
  );
}
