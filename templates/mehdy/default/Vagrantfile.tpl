# -*- mode: ruby -*-
# vi: set ft=ruby

# created by Mehdy Khoshnoody

VAGRANTFILE_API_VERSION = "2"

Vagrant.require_version ">= 1.6.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
	{% if postgres %}
	config.vm.define "postgres" do |a|
		a.vm.provider :docker do |d|
			d.image = "postgres"
			d.env = {
					POSTGRES_USER: "{{ postgres_user }}",
					POSTGRES_PASSWORD: "{{ postgres_pass }}",
					POSTGRES_DB: "{{ postgres_db }}"
			}
			d.name = "postgres_{{ name }}"
			d.ports = ["5432:5432"]
		end
	end
	{% endif %}

    {% if redis %}
	config.vm.define "redis" do |a|
		a.vm.provider :docker do |d|
			d.image = "redis"
			d.name = "redis_{{ name }}"
			d.create_args = ["-d"]
			d.ports = ["6379:6379"]
		end
	end
	{% endif %}

	config.vm.define "dev-box" do |a|
		a.vm.provider :docker do |d|
			d.build_dir = "."
			d.build_args = ['-t', 'mehdy/dev-box:{{  name }}']
			d.name = "dev_box_{{ name }}"
			d.env = {
					PG_HOSTNAME: "postgres",
					PG_USERNAME: "{{ postgres_user }}",
					PG_PASSWORD: "{{ postgres_pass }}"
			}
			d.link "postgres_{{ name }}:postgres"
			d.link "redis_{{ name }}:redis"
			d.has_ssh = true
			d.ports = ["5000:5000"]
		end
		a.ssh.port = 22
		a.ssh.username = 'root'
		a.ssh.password = 'toor'
		a.vm.synced_folder ".", "/project"
	end
end