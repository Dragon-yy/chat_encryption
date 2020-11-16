create table `user`(
 `uid` bigint(20) not null auto_increment comment '用户uid',
 `nickname` varchar(100) not null default '' comment '用户名',
 `mobile` varchar(20) not null default '' comment '手机号码',
 `email` varchar(100) not null default '' comment '邮箱地址',
 `sex` tinyint(1) not null default '0' comment '1：男 2：女 0：没填写',
 `avatar` varchar(64) not null default 'default.jpeg' comment '头像',
 `login_name` varchar(20) not null default '' comment '登陆用户名',
 `login_pwd` varchar(32) not null default '' comment '登陆密码',
 `login_salt` varchar(32) not null default '' comment '登陆密码的随机加密密钥',
 `status` tinyint(1) not null default '1' comment '1：有效 2：无效',
 `updated_time` timestamp not null default '0000-00-00 00:00:00' comment '最后一次更新时间',
 `created_time` timestamp not null default '0000-00-00 00:00:00' comment '插入时间',
 primary key (`uid`),
 unique key `login_name` (`login_name`)
) engine=InnoDB default charset=utf8 comment='用户表（管理员）';


