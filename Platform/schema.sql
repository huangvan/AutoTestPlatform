DROP TABLE IF EXISTS `caselist`;
CREATE TABLE IF NOT EXISTS `caselist` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `user_id` int(16) NOT NULL,
  `user_name` varchar(24) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `server` varchar(256) NOT NULL,
  `mock_status` int(2) NOT 0 COMMENT '是否已经录制接口',
  `status` int(2) NOT 0 COMMENT '测试结果',
  `reset_status` int(2) NOT 0 COMMENT '重置标志',
  `script` longtext,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into caselist(id, user_id, user_name, title, server, mock_status, status, reset_status, script, create_time) values(1, 1, 'admin', '商城直接购买商品，白条支付', 'QDD', '0', '0', '0', '',1549639959), (2, 1, 'admin', '商城直接购买商品，挂账支付', 'QDD', '1', '1', '1', '', 1549640336), (3, 1, 'admin', '商城直接购买商品，微信支付', 'QDD', '1', '0', '0', '',1549640355);

DROP TABLE IF EXISTS `base_user`;
CREATE TABLE `base_user` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) DEFAULT NULL,
  `password` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

insert into base_user values(1, 'admin', 'admin');
insert into base_user values(2, 'ban', 'ban');

