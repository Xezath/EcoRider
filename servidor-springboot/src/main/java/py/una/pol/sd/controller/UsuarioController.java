package py.una.pol.sd.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import py.una.pol.sd.model.Usuario;
import py.una.pol.sd.service.UsuarioService;

@RestController
@RequestMapping("/api/usuarios")
public class UsuarioController {

    @Autowired
    UsuarioService service;

    // GET /api/usuarios/listar -> listar todos los usuarios
    @GetMapping(value = "/listar", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Usuario>> listar() {
        List<Usuario> lista = service.listar();
        return new ResponseEntity<>(lista, HttpStatus.OK);
    }

    // GET /api/usuarios/{id} -> obtener usuario por id
    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Usuario> obtenerPorId(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(u -> new ResponseEntity<>(u, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // POST /api/usuarios/crear -> crear usuario
    @PostMapping(value = "/crear", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Usuario> crear(@RequestBody Usuario u) {
        Usuario nuevo = service.guardar(u);
        return new ResponseEntity<>(nuevo, HttpStatus.CREATED);
    }

    // PUT /api/usuarios/actualizar/{id} -> actualizar usuario
    @PutMapping(value = "/actualizar/{id}", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Usuario> actualizar(@PathVariable Long id, @RequestBody Usuario u) {
        return service.buscarPorId(id)
                .map(existing -> {
                    existing.setNombre(u.getNombre());
                    existing.setEmail(u.getEmail());
                    existing.setTelefono(u.getTelefono());
                    existing.setVehiculoId(u.getVehiculoId());
                    Usuario updated = service.guardar(existing);
                    return new ResponseEntity<>(updated, HttpStatus.OK);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    // DELETE /api/usuarios/eliminar/{id} -> eliminar usuario
    @DeleteMapping("/eliminar/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        return service.buscarPorId(id)
                .map(u -> {
                    service.eliminar(id);
                    return new ResponseEntity<Void>(HttpStatus.NO_CONTENT);
                }).orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
}