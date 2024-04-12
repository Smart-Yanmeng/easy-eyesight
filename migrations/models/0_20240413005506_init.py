from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `org` (
    `org_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '机构ID',
    `org_name` VARCHAR(64) NOT NULL  COMMENT '机构名',
    `org_type` INT NOT NULL  COMMENT '机构类型'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(16) NOT NULL  COMMENT '用户名',
    `face_img` LONGBLOB NOT NULL  COMMENT '照片',
    `create_time` VARCHAR(64) NOT NULL  COMMENT '创建时间',
    `org_id` BIGINT NOT NULL,
    CONSTRAINT `fk_user_org_07018d17` FOREIGN KEY (`org_id`) REFERENCES `org` (`org_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
